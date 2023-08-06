"""
Normalize KGTK edge file by removing additional columns that match the "lift" pattern..
"""
from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles
from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.lift.kgtklift import KgtkLift
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalue import KgtkValue
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Normalize a KGTK edge file by reversing the "lift" pattern or converting escondary edge columns to new edges.',
        'description': 'Normalize a KGTK edge file by removing columns that match a "lift" pattern and converting remaining additional columns to new edges.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """

    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_input_file(positional=True)
    parser.add_output_file()
    parser.add_output_file(who="An optional output file for new edges (normalized and/or lowered). " +
                           "If omitted, new edges will go in the main output file.",
                           dest="new_edges_file",
                           options=["--new-edges-file"],
                           metavar="NEW_EDGES_FILE",
                           optional=True)


    parser.add_argument(      "--columns", "--columns-to-lower", "--columns-to-remove", action="store", type=str, dest="columns_to_lower", nargs='+',
                              help="Columns to lower and remove as a space-separated list. (default=all columns other than key columns)")

    parser.add_argument(      "--base-columns", dest="base_columns",
                              help=h("Optionally, explicitly list the base column for each column being lowered. " +
                              " --base-columns and --columns-to-lower must have the same number of entries."), nargs='*')

    parser.add_argument(      "--label-value", action="store", type=str, dest="label_value",
                              help=h("The label value to use for lowered edges when --base-columns is used. (default=%(default)s)"),
                              default=KgtkLift.DEFAULT_LABEL_SELECT_COLUMN_VALUE)

    parser.add_argument(      "--lift-separator", dest="lift_separator",
                              help=h("The separator between the base column and the label value. (default=%(default)s)."),
                              default=KgtkLift.DEFAULT_OUTPUT_LIFTED_COLUMN_SEPARATOR)

    parser.add_argument(      "--lower", dest="lower",
                              help="When True, lower columns that match a lift pattern. (default=%(default)s)",
                              type=optional_bool, nargs='?', const=True, default=True, metavar="True|False")

    parser.add_argument(      "--normalize", dest="normalize",
                              help="When True, normalize columns that do not match a lift pattern. (default=%(default)s)",
                              type=optional_bool, nargs='?', const=True, default=True, metavar="True|False")

    parser.add_argument(      "--deduplicate-new-edges", dest="deduplicate_new_edges",
                              help="When True, deduplicate new edges. Not suitable for large files. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True, metavar="True|False")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, default_mode=KgtkReaderMode.EDGE, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        new_edges_file: KGTKFiles,

        base_columns: typing.Optional[typing.List[str]] = None,
        columns_to_lower: typing.Optional[typing.List[str]] = None,
        label_value: str = KgtkLift.DEFAULT_LABEL_SELECT_COLUMN_VALUE,
        lift_separator: str = KgtkLift.DEFAULT_OUTPUT_LIFTED_COLUMN_SEPARATOR,
        lower: bool = False,
        normalize: bool = False,
        deduplicate_new_edges: bool = True,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from kgtk.exceptions import kgtk_exception_auto_handler, KGTKException

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
    new_edges_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(new_edges_file, who="Label file")

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file)
        if new_edges_kgtk_file is not None:
            print("--label-file=%s" % str(new_edges_kgtk_file), file=error_file)

        if base_columns is not None:
            print("--base-columns=%s" % " ".join(base_columns), file=error_file)
        if columns_to_lower is not None:
            print("--columns-to-lower=%s" % " ".join(columns_to_lower), file=error_file)
        print("--label-value=%s" % label_value, file=error_file)
        print("--lift-separator=%s" % lift_separator, file=error_file)
        print("--lower=%s" % lower, file=error_file)
        print("--normalize=%s" % normalize, file=error_file)
        print("--deduplicate-labels=%s" % deduplicate_new_edges, file=error_file)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)


    if not lower and not normalize:
        raise KGTKException("One or both of --lower and --normalize must be requested.")

    try:
        if verbose:
            print("Opening the input file: %s" % str(input_kgtk_file), file=error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         options=reader_options,
                                         value_options = value_options,
                                         error_file=error_file,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
        )

        # Map the index of a column being removed to the index of the base column that supplies its node1 value.
        lower_map: typing.MutableMapping[int, typing.Tuple[int, str]] = dict()

        node1_column_name: str = kr.get_node1_column_actual_name()
        label_column_name: str = kr.get_label_column_actual_name()
        node2_column_name: str = kr.get_node2_column_actual_name()
        id_column_name: str = kr.get_id_column_actual_name()

        key_column_names: typing.List[str] = list()
        key_column_idxs: typing.Set[int] = set()

        if node1_column_name != "":
            if verbose:
                print("Node1 column name: %s" % node1_column_name, file=error_file, flush=True)
            key_column_names.append(node1_column_name)
            key_column_idxs.add(kr.node1_column_idx)
            
        if label_column_name != "":
            if verbose:
                print("Label column name: %s" % label_column_name, file=error_file, flush=True)
            key_column_names.append(label_column_name)
            key_column_idxs.add(kr.label_column_idx)
            
        if node2_column_name != "":
            if verbose:
                print("Node2 column name: %s" % node2_column_name, file=error_file, flush=True)
            key_column_names.append(node2_column_name)
            key_column_idxs.add(kr.node2_column_idx)
            
        if id_column_name != "":
            if verbose:
                print("Id column name: %s" % id_column_name, file=error_file, flush=True)
            key_column_names.append(id_column_name)
            key_column_idxs.add(kr.id_column_idx)
        elif normalize:
            raise KGTKException("--normalize was requested but the ID column was not found.")
  
        base_name: str
        new_label_value: str
        column_name: str
        idx: int
        # There are three option patterns.

        if columns_to_lower is not None and len(columns_to_lower) > 0 and base_columns is not None and len(base_columns) > 0:
            # Pattern 1: len(columns_to_lower) > 0 and len(base_columns) == len(columns_to_lower)
            # column_names and base_columns are paired. New records use label_value.
            if len(columns_to_lower) != len(base_columns):
                raise KGTKException("There are %d columns to remove but only %d base columns." % (len(columns_to_lower), len(base_columns)))
        
            if len(label_value) == 0:
                raise KGTKException("The --label-value must not be empty.")

            for idx, column_name in enumerate(columns_to_lower):
                base_name = base_columns[idx]
                if column_name not in kr.column_names:
                    raise KGTKException("Column %s is an unknown column, cannot remove it." % repr(column_name))

                if column_name in key_column_names:
                    raise KGTKException("Column %s is a key column, cannot remove it." % repr(column_name))

                if base_name not in kr.column_names:
                    raise KGTKException("For column name %s, base name %s is unknown" % (repr(column_name), repr(base_name)))

                if normalize and base_name == id_column_name:
                    lower_map[kr.column_name_map[column_name]] = (kr.column_name_map[base_name], column_name)
                else:
                    if not lower:
                        raise KGTKException("--lower is not enabled for column %s, base name %s" % (repr(column_name), repr(base_name)))
                    lower_map[kr.column_name_map[column_name]] = (kr.column_name_map[base_name], label_value)

        elif columns_to_lower is not None and len(columns_to_lower) > 0 and (base_columns is None or len(base_columns) == 0):
            # Pattern 2: len(columns_to_lower) > 0 and len(base_columns) == 0
            # Each column name is split at the lift separator to determine the base name and label value.
            if len(lift_separator) == 0:
                raise KGTKException("The --lift-separator must not be empty.")

            for idx, column_name in enumerate(columns_to_lower):
                if column_name not in kr.column_names:
                    raise KGTKException("Column %s is an unknown column, cannot remove it." % repr(column_name))

                if column_name in key_column_names:
                    raise KGTKException("Column %s is a key column, cannot remove it." % repr(column_name))

                if lower and lift_separator in column_name:
                    base_name, new_label_value = column_name.split(lift_separator, 1)
                    if base_name not in kr.column_names:
                        raise KGTKException("For column name %s, base name %s is not known" % (repr(column_name), repr(base_name)))

                elif normalize:
                    base_name = id_column_name
                    new_label_value = column_name

                else:
                    raise KGTKException("Unable to parse column name %s, no separator (%s)." % (repr(column_name), repr(lift_separator)))

                lower_map[kr.column_name_map[column_name]] = (kr.column_name_map[base_name], new_label_value)

        elif columns_to_lower is None or len(columns_to_lower) == 0:
            # Pattern 3: len(columns_to_lower) == 0.
            # Any column that matches a lift pattern against one of the
            # key columns (node1, label, node2, id, or their aliases)
            # will be lowered.
            if len(lift_separator) == 0:
                raise KGTKException("The --lift-separator must not be empty.")

            if base_columns is None or len(base_columns) == 0:
                # The base name list wasn't supplied.  Use [node1, label, node2, id]
                base_columns = list(key_column_names)
                if verbose:
                    print("Using the default base columns: %s" % " ".join(base_columns), file=error_file, flush=True)
            else:
                if verbose:
                    print("Using these base columns: %s" % " ".join(base_columns), file=error_file, flush=True)

            for idx, column_name in enumerate(kr.column_names):
                # Skip the node1, label, node12, and id columns
                if idx in key_column_idxs:
                    if verbose:
                        print("column %s is a key column, skipping." % repr(column_name), file=error_file, flush=True)
                    continue

                # Does this column match a lifting pattern?
                if lower and lift_separator in column_name:
                    base_name, new_label_value = column_name.split(lift_separator, 1)

                    if base_name not in base_columns:
                        if verbose:
                            print("Column %s contains base name %s, which is not a base column." % (repr(column_name), repr(base_name)),  file=error_file, flush=True)
                        continue
                                  
                elif normalize:
                    base_name = id_column_name
                    new_label_value = column_name

                else:
                    if verbose:
                        print("Column %s does not contain the separator %s and not normalizing, skipping." % (repr(column_name), repr(lift_separator)), file=error_file, flush=True)
                    continue

                # This test should be redundant.
                if base_name in kr.column_names:
                    lower_map[idx] = (kr.column_name_map[base_name], new_label_value)
                else:
                    raise KGTKException("Base name %s was unexpectedly not found." % repr(base_name))

        if len(lower_map) == 0:
            raise KGTKException("There are no columns to lower or normalize.")

        if verbose:
            print("The following columns will be lowered or normalized", file=error_file, flush=True)
            for idx in sorted(lower_map.keys()):
                column_name = kr.column_names[idx]
                base_idx, new_label_value = lower_map[idx]
                base_name = kr.column_names[base_idx]
                print(" %s from %s (label %s)" % (column_name, base_name, repr(new_label_value)), file=error_file, flush=True)

        output_column_names: typing.List[str] = list()
        for idx, column_name in enumerate(kr.column_names):
            if idx not in lower_map:
                output_column_names.append(column_name)
        if verbose:
            print("The output columns are: %s" % " ".join(output_column_names), file=error_file, flush=True)

        if verbose:
            print("Opening the output file: %s" % str(output_kgtk_file), file=error_file, flush=True)
        kw: KgtkWriter = KgtkWriter.open(output_column_names,
                                         output_kgtk_file,
                                         mode=KgtkWriter.Mode.EDGE,
                                         require_all_columns = False, # Simplifies writing the labels
                                         verbose=verbose,
                                         very_verbose=very_verbose)
        shuffle_list: typing.List[int] = kw.build_shuffle_list(kr.column_names)

        lkw: typing.Optional[KgtkWriter] = None
        if new_edges_kgtk_file is not None:
            if verbose:
                print("Opening the label output file: %s" % str(new_edges_kgtk_file), file=error_file, flush=True)

            label_column_names = [ node1_column_name, label_column_name, node2_column_name ]                
            lkw = KgtkWriter.open(label_column_names,
                                  new_edges_kgtk_file,
                                  mode=KgtkWriter.Mode.EDGE,
                                  verbose=verbose,
                                  very_verbose=very_verbose)
                      

        # Optionally deduplicate the labels
        #  set(node1_value + KgtkFormat.SEPARATOR + node2_value)
        label_set: typing.Set[str] = set()
        label_key: str

        input_line_count: int = 0
        output_line_count: int = 0
        label_line_count: int = 0
        row: typing.List[str]
        for row in kr:
            input_line_count += 1

            kw.write(row, shuffle_list=shuffle_list)
            output_line_count += 1

            column_idx: int
            for column_idx in lower_map.keys():
                node1_idx: int
                node1_idx, new_label_value = lower_map[column_idx]
                node1_value: str
                node1_value = row[node1_idx]
                if len(node1_value) == 0:
                    continue # TODO: raise an exception

                item: str = row[column_idx]
                if len(item) == 0:
                    continue # Ignore empty node2 values.

                # Ths item might be a KGTK list.  Let's split it, because
                # lists aren't allow in the node2 values we'll generate.
                node2_value: str
                for node2_value in KgtkValue.split_list(item):
                    if len(node2_value) == 0:
                        continue # Ignore empty node2 values.

                    if deduplicate_new_edges:
                        label_key = node1_value + KgtkFormat.KEY_FIELD_SEPARATOR + new_label_value + KgtkFormat.KEY_FIELD_SEPARATOR + node2_value
                        if label_key in label_set:
                            continue
                        else:
                            label_set.add(label_key)

                    output_map: typing.Mapping[str, str] = {
                        node1_column_name: node1_value,
                        label_column_name: new_label_value,
                        node2_column_name: node2_value,
                    }
                    if lkw is None:
                        kw.writemap(output_map)
                        label_line_count += 1
                        output_line_count += 1
                    else:
                        lkw.writemap(output_map)
                        label_line_count += 1

        if verbose:
            print("Read %d rows, wrote %d rows with %d labels." % (input_line_count, output_line_count, label_line_count), file=error_file, flush=True)

        kw.close()
        if lkw is not None:
            lkw.close()

        return 0

    except Exception as e:
        kgtk_exception_auto_handler(e)
        return 1
