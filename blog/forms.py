from django import forms
from .models import BlogPost

#class BlogPostForm(forms.ModelForm):
    #class Meta:
        #Model = BlogPost
        #fields = ('title','slug','content','image')
        #widgets = {
            #'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Titlle of the Blog'}),
            #'slug': forms.TextInput(attrs={'class':'form-control','placeholder':'copy the title with no space and hyphen'}),
            #'content': forms.Textarea(attrs={'class':'form-control','placeholder':'Content of the blog'}),
        #}

class SendEmailForm(forms.Form):
    email = forms.EmailField()      