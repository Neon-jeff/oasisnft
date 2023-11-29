from django.db import models

# Create your models here.
from django.db import models
from io import BytesIO
import sys
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    verified=models.BooleanField(default=False)
    token=models.CharField(blank=True,null=True,max_length=300)
    avatar=CloudinaryField('image',blank=True,null=True)
    full_name=models.CharField(max_length=100,null=True,blank=True)
    wallet_address=models.CharField(max_length=100,null=True,blank=True)
    balance=models.FloatField(default=0.00,null=True,blank=True)
    can_withdraw=models.BooleanField(default=False,blank=True,null=True)
    can_own=models.BooleanField(default=False,blank=True,null=True)

    def save(self,*args,**kwargs):
            # compress nft_file
        # if self.avatar:
        #     im = Image.open(self.avatar)

        #     output = BytesIO()

        # # Resize/modify the image
        #     original_width, original_height = im.size
        #     if(original_width >200 or original_height>200):
        #         aspect_ratio = round(original_width / original_height)
        #         desired_height = 200  # Edit to add your desired height in pixels
        #         desired_width = desired_height * aspect_ratio

        # # Resize the image
        #         im = im.resize((desired_width, desired_height))

        # # after modifications, save it to the output
        #     im.save(output, format='PNG', quality=80)
        #     output.seek(0)

        # # change the imagefield value to be the newley modifed image value
        #     self.avatar = InMemoryUploadedFile(output, 'CloudinaryField', "%s.png" % self.avatar.name.split('.')[0], 'image/png',
        #                                 sys.getsizeof(output), None)
        super(UserProfile, self).save(*args, **kwargs)
    def __str__(self):
        return self.user.username + 'profile'

class NFT(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='nft')
    name=models.CharField(max_length=50,default='')
    nft_file=CloudinaryField('image',blank=True,null=True)
    price=models.FloatField(blank=True,null=True,default=0.00)
    minted=models.BooleanField(default=False)
    gas_fee=models.FloatField(blank=True,null=True)
    sold=models.BooleanField(default=False)
    on_sale=models.BooleanField(default=False)
    description=models.TextField(max_length=500,default='')
    supply=models.IntegerField(blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    pending=models.BooleanField(default=False,null=True,blank=True)
    amount_sold=models.IntegerField(default=0,null=True,blank=True)
    image_url=models.URLField(max_length=400,blank=True,null=True)
    def save(self,*args,**kwargs):
        # compress nft_file
        # im = Image.open(self.nft_file)

        # output = BytesIO()

        # # Resize/modify the image
        # original_width, original_height = im.size
        # if(original_width >600 or original_height>600):
        #     aspect_ratio = round(original_width / original_height)
        #     desired_height = 600  # Edit to add your desired height in pixels
        #     desired_width = desired_height * aspect_ratio

        # # Resize the image
        #     im = im.resize((desired_width, desired_height))

        # # after modifications, save it to the output
        # im.save(output, format='JPEG', quality=80)
        # output.seek(0)

        # # change the imagefield value to be the newley modifed image value
        # self.nft_file = InMemoryUploadedFile(output, 'CloudinaryField', "%s.jpg" % self.nft_file.name.split('.')[0], 'image/jpeg',
        #                                 sys.getsizeof(output), None)
        if self.minted==True:
            self.pending=False
        old_inst=NFT.objects.filter(id=self.id).first()
        if old_inst is not None:
            old_amount=old_inst.amount_sold
            self.user.profile.balance=self.user.profile.balance + float(int(self.amount_sold-old_amount)*self.price)
            self.user.profile.save()
        super(NFT, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.user.username} NFT {self.name}'

class MintingPayment(models.Model):
    nft=models.ForeignKey(NFT,on_delete=models.CASCADE,related_name='mint_payment')
    created=models.DateTimeField(auto_now_add=True)
    image_url=models.URLField(blank=True,null=True)
    confirmed=models.BooleanField(default=False,null=True,blank=True)
    def save(self,*args,**kwargs):
        if self.confirmed:
            History.objects.create(
                title="NFT Minted",
                details=f"Hi {self.nft.user.username}, your minting payment for {self.nft.name} NFT has beem confirmed",
                user=self.nft.user
            )
            self.nft.minted=True
            self.nft.pending=False
            self.nft.save()
        else:
            History.objects.create(
            title='Minting Fee Created',
            details=f"Hi {self.nft.user.username}, Minting payment for {self.nft.name} NFT created, wait for confirmations",
            user=self.nft.user,
        )
        super(MintingPayment, self).save(*args, **kwargs)
    def __str__(self):
        return f'Minting payment for {self.nft.name} from {self.nft.user.username}'

class VerficationFee(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    confirmed=models.BooleanField(default=False,null=True,blank=True)
    image_url=models.URLField(blank=True,null=True)
    def save():
        pass
    def __str__(self):
        return f"{self.user.username} Verfication Fee"
    def save(self,*args,**kwargs):
        if self.confirmed:
            self.user.profile.can_withdraw=True
            self.user.profile.save()
            History.objects.create(
                title="Account Upgrade fee verified",
                details=f"Hi {self.user.username}, your account upgrade has been verified, you can now withdraw your assets, LFG!!",
                user=self.user
            )
        else:
            History.objects.create(
                title="Account Upgraded Created",
                details=f'Hi {self.user.username}, your account upgrade request has been created',
                user=self.user
            )
        super(VerficationFee, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.user.username} Verification Fee'

class Withdrawal(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    amount=models.FloatField(null=True, blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    confirmed=models.BooleanField(default=False,null=True,blank=True)
    def save(self,*args,**kwargs):
        if self.confirmed ==False:
            History.objects.create(
                title="Withdraw Request Created",
                details=f'Hi {self.user.username}, you requested to withdraw {self.amount} ETH from your account',
                user=self.user
            )
        else:
            History.objects.create(
                user=self.user,
                title="Withdrawal request confirmed",
                details=f"Hi {self.user.username}, your request of {self.amount} ETH has been approved"
            )
        super(Withdrawal, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.user.username} Withdrawal request"

class MarketPlace(models.Model):
    image_url=models.URLField(blank=True,null=True)
    name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    price=models.FloatField(blank=True,null=True,default=0.00)
    def __str__(self):
        return f'{self.username} Marketplace NFT'

class History(models.Model):
    title=models.CharField(default='',max_length=50)
    created=models.DateTimeField(auto_now_add=True)
    details=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} notification'

class OwnedNFTs(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=CloudinaryField('image',blank=True,null=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    price=models.FloatField(default=0.00,null=True,blank=True)
    bought_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Owned NFT'
