from django.urls import path
from. import views
urlpatterns = [
    
    path('',views.careerhome,name='careerhome'),
    path('careernav',views.careernav,name='careernav'),
    path('pricing',views.pricing,name='pricing'),
    path('careercontact',views.careercontact,name='careercontact'),
    path('recruiterreg',views.recruiterreg,name='recruiterreg'),
    path('hiring',views.hiring,name='hiring'),
    path('candreg',views.candreg,name='candreg'),
    path('recruiterlog',views.recruiterlog,name='recruiterlog'),
    path('candlog',views.candlog,name='candlog'),
    path('jobseeker',views.jobseeker,name='jobseeker'),
    path('clog',views.clog,name='clog'),
    path('candnav',views.candnav,name='candnav'),
    path('candhome',views.candhome,name='candhome'),
    path('candpro',views.candpro,name='candpro'),
    path('rlog',views.rlog,name='rlog'),
    path('recruiterhome',views.recruiterhome,name='recruiterhome'),
    path('recruiternav',views.recruiternav,name='recruiternav'),
    path('log_out',views.log_out,name='log_out'),
    path('update_profile',views.update_profile,name='update_profile'),
    path('recupdate_profile',views.recupdate_profile,name='recupdate_profile'),
    path('recruiterpro',views.recruiterpro,name='recruiterpro'),
    path('change_pass',views.change_pass,name='change_pass'),
    path('postjob',views.postjob,name='postjob'),
    path('recruitermanage',views.recruitermanage,name='recruitermanage'),
    path('deletejob/<int:id>',views.deletejob,name='deletejob'),
    path('applyjob/<int:id>',views.applyjob,name='applyjob'),
    path('candmanage',views.candmanage,name='candmanage'),
    path('withdraw_application/<int:id>',views.withdraw_application,name='withdraw_application'),
    path('view_applications/<int:id>',views.view_applications,name='view_applications'),
    path('select/<int:id>',views.select,name='select'),
    path('reject/<int:id>',views.reject,name='reject'),
    ]