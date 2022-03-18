from django.http import HttpResponse


def get_ingredient_file(request, ingredients):
    filename = f"{request.user.username}_shopping_list.txt"
    shopping_list = f"Список покупок для: {request.user.first_name}\n\n"
    for ing in ingredients:
        shopping_list += f'{ing["ingredient__name"]}: {ing["amount"]} {ing["ingredient__measurement_unit"]}\n'

    shopping_list += "\n\nПосчитано в Foodgram"

    response = HttpResponse(shopping_list, content_type="text.txt; charset=utf-8")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
