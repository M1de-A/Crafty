from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating=forms.ChoiceField(
        choices=[(f'{i/2:g}',f'{i/2:g}') for i in range(1,11)],
        widget=forms.HiddenInput()
    )
    class Meta:
        model=Review
        fields=['rating','text']
        widgets={'text':forms.Textarea(attrs={'rows':5,'placeholder':'Расскажите о товаре и впечатлениях...'})}

    def __init__(self,*args,editing=False,**kwargs):
        super().__init__(*args,**kwargs)
        self.editing=editing
        if editing:
            self.fields['rating'].disabled=True

    def clean_rating(self):
        value=self.cleaned_data['rating']
        try: value=float(value)
        except (TypeError,ValueError): raise forms.ValidationError('Выберите оценку.')
        if value < 0.5 or value > 5 or (value*2)%1: raise forms.ValidationError('Оценка должна быть от 0.5 до 5.')
        return value
