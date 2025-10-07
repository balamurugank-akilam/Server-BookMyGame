from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # unique related_name for groups
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # unique related_name for user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class UserTypeMaster(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    role = models.CharField(max_length=100, db_column="Role")
    flag = models.BooleanField(default=True, db_column="flag")

    class Meta:
        db_table = 'userType_Master'
        managed = True
        verbose_name = 'userType_Master'
        verbose_name_plural = 'userType_Master'

    def __str__(self):
        return self.role


class UserMaster(models.Model):
    reg_id = models.AutoField(primary_key=True, db_column="Reg_Id" )
    email = models.CharField(max_length=255, db_column="email" , null=True , blank=True)
    mobile = models.CharField(max_length=20, db_column="mobile")
    alternative_mobile = models.CharField(max_length=20, null=True, blank=True, db_column="alternative_Mobile")
    password = models.CharField(max_length=255, db_column="password" , null=True , blank=True)
    blood_group = models.CharField(max_length=10, db_column="bloodGroup", null=True , blank=True)
    flag = models.BooleanField(default=True, db_column="flag", null=True , blank=True)
    user_type = models.ForeignKey(
        UserTypeMaster,
        on_delete=models.SET_NULL,  # or CASCADE depending on your logic
        null=True,
        db_column='userType'
    )  # or ForeignKey if related table exists
    image_url = models.CharField(max_length=500, null=True, blank=True, db_column="imageUrl")
    created_date = models.DateTimeField(auto_now_add=True, db_column="created_Date")
    name = models.CharField(max_length=255, db_column="name")
    grp_reg_id = models.IntegerField(null=True, blank=True, db_column="grpRegId",)
    
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user_Master'
        managed = True
        verbose_name = 'user_Master'
        verbose_name_plural = 'user_Master'



# class SportCategory(models.Model):
#     category_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=250, null=False, blank=False)
#     flag = models.BooleanField(default=False)
#     image = models.ImageField(upload_to='assets/images', default='')
    
#     class Meta:
#         db_table = 'SportCategory'
#         managed = True
#         verbose_name = 'SportCategory'
#         verbose_name_plural = 'SportCategory'

#     def __str__(self):
#         return self.name
    
    

 