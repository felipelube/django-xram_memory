from django import forms


class ArchivedNewsPDFCaptureStackedInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArchivedNewsPDFCaptureStackedInlineForm,
              self).__init__(*args, **kwargs)


class ArchivedNewsAdminForm(forms.ModelForm):
    INSERTION_AUTOMATIC = 0
    INSERTION_MANUAL = 1

    INSERTION_MODES = (
        (INSERTION_AUTOMATIC, "Inserção automática"),
        (INSERTION_MANUAL, "Inserção manual"),
    )

    insertion_mode = forms.ChoiceField(required=False,
                                       widget=forms.RadioSelect, choices=INSERTION_MODES, label="Modo de inserção")

    def __init__(self, *args, **kwargs):
        super(ArchivedNewsAdminForm, self).__init__(*args, **kwargs)
        self.initial['insertion_mode'] = self.INSERTION_AUTOMATIC
        if not self.instance.pk is None:
            self.fields['force_basic_processing'].label = "Reinserir na fila para processamento automático"
            self.fields['force_basic_processing'].help_text = "Marque se deseja reinserir essa notícia para processamento automático.<br/><strong>NOTA:</strong> isso sobrescreverá qualquer informação anterior."

            self.fields['force_archive_org_processing'].label = "Reinserir na fila para buscar informações no Archive.org"
            self.fields['force_archive_org_processing'].help_text += "<br/><strong>NOTA:</strong> isso sobrescreverá qualquer informação anterior."

            self.fields['force_pdf_capture'].label = "Gerar uma nova captura de página"
            self.fields['force_pdf_capture'].help_text += "<br/><strong>NOTA:</strong> isso substituirá a captura de página anterior."

    def clean(self):
        cleaned_data = super(ArchivedNewsAdminForm, self).clean()

        title = cleaned_data.get('title', '')
        url = cleaned_data.get('url', '')
        archived_news_url = cleaned_data.get('archived_news_url', '')
        insertion_mode = cleaned_data.get(
            'insertion_mode', self.INSERTION_AUTOMATIC)

        force_pdf_capture = cleaned_data.get('force_pdf_capture', False)
        force_archive_org_processing = cleaned_data.get(
            'force_archive_org_processing', False)
        force_basic_processing = cleaned_data.get(
            'force_basic_processing', False)

        manual_insert = insertion_mode == self.INSERTION_MANUAL or not (
            force_pdf_capture or force_archive_org_processing or force_basic_processing)

        # Se alguns dos campos acima foram alterados numa notícia prestes a ser inserida, o título deve ser definido
        if self.instance.pk is None:
            if manual_insert and not title:
                self.add_error(
                    'title', 'Você precisa dar um título para a notícia')

        # A notícia deve conter ao menos uma url, seja a original ou seja a arquivada
        if not (url or archived_news_url):
            self.add_error(
                'url', 'Preencha este campo')
            self.add_error(
                'archived_news_url', 'Preencha este campo')
            raise forms.ValidationError(
                "Você precisa definir ao menos um endereço para a notícia")