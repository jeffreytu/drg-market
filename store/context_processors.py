from .models import Category

def menuCategories(request):

    menu_categories = Category.objects.all()

    return {

        'menu_categories': menu_categories
        
    }