
from django.urls import path
from .views import *


urlpatterns = [
    path("register/",RegisterUser,name='register' ),
    path("recover-account",RecoverAccount,name='recover'),
    path("success",RegisterSuccess,name='success'),
    path('login',Login,name='login'),
    path('user/dashboard',Dashboard,name='dashboard'),
    path('user/create-nft',CreateNFT,name='create-nft'),
    path('user/mint-nft/<int:pk>',MintNFT,name='mintnft'),
    path('user/connectwallet',AddWallet,name='addwallet'),
    path('user/nft/<int:pk>',ViewNFT,name='view-nft'),
    path('user/upgrade-account',UpgradeAccount,name='upgrade'),
    path('user/withdrawal',Withdraw,name='withdraw'),
    path('user/history',UserHistory,name='history'),
    path('user/logout',Logout,name='logout'),
    path('user/activate/',Activate,name='activate'),
    path('verify-success',VerifySuccess,name='vsuccess'),
    path('user/avatar',UpdateAvatar,name='avatar'),
    path('user/own-nft',OwnNFT,name='own')
]
