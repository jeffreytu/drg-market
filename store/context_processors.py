from .models import Category

def menuCategories(request):

    menu_categories = Category.objects.select_related('parent').all()
    iphones = menu_categories.get(slug='apple-iphone').get_children()
    samsungs = menu_categories.get(slug='samsung').get_children()

    return {

        'menu_categories': menu_categories,
        'iphones': iphones,
        'samsungs': samsungs,
        
    }