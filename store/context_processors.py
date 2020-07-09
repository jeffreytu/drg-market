from .models import Category

def menuCategories(request):

    menu_categories = Category.objects.select_related('parent').all()
    iphones = menu_categories.get(slug='apple-iphone').get_children()

    print(iphones)

    return {

        'menu_categories': menu_categories,
        'iphones': iphones,
        
    }