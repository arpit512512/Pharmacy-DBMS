from django import forms

class AddCartForm(forms.Form):
	qty = forms.CharField()

	def clean_qty(self):
		qty = self.cleaned_data.get('qty')
		return qty

		