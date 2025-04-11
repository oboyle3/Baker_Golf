# from django import forms
# from .models import User

# class SignUpForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['name', 'email', 'age', 'password']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])  # Hash password
#         if commit:
#             user.save()
#         return user
from .models import User, Golfer, AllUsersFavoriteGolfers
from django import forms
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['name', 'email', 'age', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash password
        if commit:
            user.save()

        # Manually specify the golfer IDs you want to assign (IDs 1, 4, 5, 10)
        default_golfer_ids = [11, 25, 37, 48]

        # Loop through the golfer IDs and create entries in the favorite golfers table
        for golfer_id in default_golfer_ids:
            AllUsersFavoriteGolfers.objects.create(user_id=user.id, golfer_id=golfer_id)
        
        return user


class FavoriteGolfersForm(forms.Form):
    golfers = forms.ModelMultipleChoiceField(
        queryset=Golfer.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
