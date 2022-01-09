from django import forms 

  
class uploadform(forms.Form): 
    imgfile=forms.FileField()

# class uploadform1(forms.Form): 
#     vidfile=forms.FileField()
  
    