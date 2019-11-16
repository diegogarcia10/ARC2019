from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout, login as lg
# Create your views here.
def login(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		err = ""	
		if request.method == 'POST':
		    username = request.POST.get('username',False)
		    password = request.POST.get('password',False)	    
		    user = authenticate(request, username=username, password=password)
		    if user is not None:
		        lg(request, user)
		        return redirect('hospital:index2')	        
		    else:
		    	err = "Error al ingresar credenciales, Asegurese de que el usuario y contraseña esten escritas correctamente"
		    	return render(request, 'autentificacion/login.html',{'err':err})
		else:
			return render(request, 'autentificacion/login.html')

	

def logout_v(request):
    logout(request)
    return redirect('hospital:index')