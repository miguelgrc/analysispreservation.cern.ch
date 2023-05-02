import TextWidget from "./TextWidget";
import SelectWidget from "./SelectWidget";
import RichEditorWidget from "./RichEditorWidget";
import SwitchWidget from "./SwitchWidget";
import CheckboxWidget from "./CheckboxWidget";
import UriWidget from "./UriWidget";
import DateWidget from "./DateWidget";
import RequiredWidget from "./containers/RequiredWidget";

const widgets = {
  text: TextWidget,
  uri: UriWidget,
  select: SelectWidget,
  latex: RichEditorWidget,
  richeditor: RichEditorWidget,
  switch: SwitchWidget,
  checkbox: CheckboxWidget,
  date: DateWidget,
  required: RequiredWidget,
};

export default widgets;
