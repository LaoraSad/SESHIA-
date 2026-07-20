from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'finances'

urlpatterns = [
    path('', views.TransactionListView.as_view(), name='list'),
    path('agregar/', RedirectView.as_view(pattern_name='finances:create-expense'), name='add-transaction'),
    path('crear-gasto/', views.CreateExpenseView.as_view(), name='create-expense'),
    path('crear-ingreso/', views.CreateIncomeView.as_view(), name='create-income'),
    path('editar/<int:transaction_id>/', views.UpdateTransactionView.as_view(), name='update-transaction'),
    path('eliminar/<int:transaction_id>/', views.DeleteTransactionView.as_view(), name='delete-transaction'),
    path('categorias/', views.CategoryListView.as_view(), name='category-list'),
    path('categorias/crear/', views.CreateCategoryView.as_view(), name='create-category'),
    path('categorias/editar/<int:category_id>/', views.UpdateCategoryView.as_view(), name='update-category'),
    path('categorias/eliminar/<int:category_id>/', views.DeleteCategoryView.as_view(), name='delete-category'),
]
