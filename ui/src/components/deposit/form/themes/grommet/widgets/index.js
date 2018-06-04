import TextWidget from './TextWidget';
import SelectWidget from './SelectWidget';
import UpDownWidget from './UpDownWidget';
import RadioWidget from './RadioWidget';
import CheckboxWidget from './CheckboxWidget';
import AutocompleteWidget from './AutocompleteWidget';

const widgets = {
    text: TextWidget,
    select: SelectWidget,
    updown: UpDownWidget,
    radio: RadioWidget,
    checkboxes: CheckboxWidget,
    autocomplete: AutocompleteWidget
};

export default widgets;
