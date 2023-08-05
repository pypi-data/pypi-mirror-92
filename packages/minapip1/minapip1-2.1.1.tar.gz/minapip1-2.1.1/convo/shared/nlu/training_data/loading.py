import json
import logging
import os
import typing
from typing import Optional, Text

import convo.shared.utils.io
from convo.shared.nlu.training_data.formats import MarkdownReader, NLGMarkdownReader
from convo.shared.nlu.training_data.formats.dialogflow import (
    DIALOGFLOW_AGENT,
    DIALOGFLOW_ENTITIES,
    DIALOGFLOW_ENTITY_ENTRIES,
    DIALOGFLOW_INTENT,
    DIALOGFLOW_INTENT_EXAMPLES,
    DIALOGFLOW_PACKAGE,
)
from convo.shared.nlu.training_data.training_data import TrainingData

if typing.TYPE_CHECKING:
    from convo.shared.nlu.training_data.formats.readerwriter import TrainingDataReader

logger = logging.getLogger(__name__)

# Different supported file formats and their identifier
WIT = "wit"
LUIS = "luis"
CONVO = "convo_nlu"
MARKDOWN = "md"
CONVO_YAML = "convo_yml"
UNK = "unk"
MARKDOWN_NLG = "nlg.md"
JSON = "json"
DIALOGFLOW_RELEVANT = {DIALOGFLOW_ENTITIES, DIALOGFLOW_INTENT}

_json_format_heuristics = {
    WIT: lambda js, fn: "data" in js and isinstance(js.get("data"), list),
    LUIS: lambda js, fn: "luis_schema_version" in js,
    CONVO: lambda js, fn: "convo_nlu_data" in js,
    DIALOGFLOW_AGENT: lambda js, fn: "supportedLanguages" in js,
    DIALOGFLOW_PACKAGE: lambda js, fn: "version" in js and len(js) == 1,
    DIALOGFLOW_INTENT: lambda js, fn: "responses" in js,
    DIALOGFLOW_ENTITIES: lambda js, fn: "isEnum" in js,
    DIALOGFLOW_INTENT_EXAMPLES: lambda js, fn: "_usersays_" in fn,
    DIALOGFLOW_ENTITY_ENTRIES: lambda js, fn: "_entries_" in fn,
}


def load_data(resource_name: Text, language: Optional[Text] = "en") -> "TrainingData":
    """Load training data from disk.

    Merges them if loaded from disk and multiple files are found."""
    if not os.path.exists(resource_name):
        raise ValueError(f"File '{resource_name}' does not exist.")

    if os.path.isfile(resource_name):
        files = [resource_name]
    else:
        files = convo.shared.utils.io.list_files(resource_name)

    data_sets = [_load(f, language) for f in files]
    data_sets = [ds for ds in data_sets if ds]
    if len(data_sets) == 0:
        training_data = TrainingData()
    elif len(data_sets) == 1:
        training_data = data_sets[0]
    else:
        training_data = data_sets[0].merge(*data_sets[1:])

    return training_data


def _reader_factory(fformat: Text) -> Optional["TrainingDataReader"]:
    """Generates the appropriate reader class based on the file format."""
    from convo.shared.nlu.training_data.formats import (
        ConvoYAMLReader,
        MarkdownReader,
        WitReader,
        LuisReader,
        ConvoReader,
        DialogflowReader,
        NLGMarkdownReader,
    )

    reader = None
    if fformat == LUIS:
        reader = LuisReader()
    elif fformat == WIT:
        reader = WitReader()
    elif fformat in DIALOGFLOW_RELEVANT:
        reader = DialogflowReader()
    elif fformat == CONVO:
        reader = ConvoReader()
    elif fformat == MARKDOWN:
        reader = MarkdownReader()
    elif fformat == MARKDOWN_NLG:
        reader = NLGMarkdownReader()
    elif fformat == CONVO_YAML:
        reader = ConvoYAMLReader()
    return reader


def _load(filename: Text, language: Optional[Text] = "en") -> Optional["TrainingData"]:
    """Loads a single training data file from disk."""

    fformat = guess_format(filename)
    if fformat == UNK:
        raise ValueError(f"Unknown data format for file '{filename}'.")

    reader = _reader_factory(fformat)

    if reader:
        return reader.read(filename, language=language, fformat=fformat)
    else:
        return None


def guess_format(filename: Text) -> Text:
    """Applies heuristics to guess the data format of a file.

    Args:
        filename: file whose type should be guessed

    Returns:
        Guessed file format.
    """
    from convo.shared.nlu.training_data.formats import ConvoYAMLReader

    guess = UNK

    if not os.path.isfile(filename):
        return guess

    try:
        content = convo.shared.utils.io.read_file(filename)
        js = json.loads(content)
    except ValueError:
        if MarkdownReader.is_markdown_nlu_file(filename):
            guess = MARKDOWN
        elif NLGMarkdownReader.is_markdown_nlg_file(filename):
            guess = MARKDOWN_NLG
        elif ConvoYAMLReader.is_yaml_nlu_file(filename):
            guess = CONVO_YAML
    else:
        for file_format, format_heuristic in _json_format_heuristics.items():
            if format_heuristic(js, filename):
                guess = file_format
                break

    logger.debug(f"Training data format of '{filename}' is '{guess}'.")

    return guess
