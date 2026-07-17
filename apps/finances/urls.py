from django.urls import path
from . import views

app_name = 'finances'

urlpatterns = [
    path('finances/', views.FinancesView.as_view(), name='finances'),
    path('api/finances/add/', views.AddTransactionView.as_view(), name='add-transaction'),
    path('api/finances/delete/<int:id>/', views.DeleteTransactionView.as_view(), name='delete-transaction'),
    path("api/finances/edit/<int:id>/", views.EditTransactionView.as_view(), name="edit-transaction"),
]