from cement.utils.shell import Prompt


class LiftoffPrompt(Prompt):
    class Meta:
        numbered = True
        selection_text = ">"

    def __init__(self, text=None, *args, **kw):
        if text is not None:
            if 'default' in kw.keys():
                if kw.get('numbered') is False:
                    text = f"{text} [default: {kw.get('default')}]"
                else:
                    default = kw.get('default')
                    default_text = str(default)

                    if 'options' in kw.keys():
                        options = kw.get('options')
                        default_text = options[int(default) - 1]

                    text = f"{text} [default: {default_text}]"

            if 'options' not in kw.keys():
                text = f"{text}\n\n>"

        super(LiftoffPrompt, self).__init__(text, *args, **kw)

    def process_input(self):
        print()