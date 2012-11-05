from django import forms


class UploadFileForm(forms.Form):
    ''' simple form class for mindmap file upload
    
    '''
    mmfile = forms.FileField(
        label='Select a file'
    )
