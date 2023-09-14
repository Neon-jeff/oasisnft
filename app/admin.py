from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(UserProfile)
admin.site.register(NFT)
admin.site.register(MintingPayment)
admin.site.register(VerficationFee)
admin.site.register(MarketPlace)
admin.site.register(Withdrawal)
admin.site.register(History)
admin.site.register(OwnedNFTs)
