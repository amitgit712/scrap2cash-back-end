from django.urls import path
from admin_dashboard.views import(
	admin_dashboard,
	admin_login,logout_view,
	view_post,approve_post,
	suggest_changes,suspend_post,
	users,user_deatail,all_approve_post,all_unapprove_post,
	all_suspended_post,unapprove,unsuspend_post
	)

app_name="admin_dashboard"

urlpatterns = [
	path('admin_dashboard/',admin_dashboard, name="admin_dashboard"),
	path('admin_login/',admin_login, name="admin_login"),
	path('logout/',logout_view,name="logout"),
	path('view_post/<post_id>/',view_post,name="view_post"),
	path('approve_post/<post_id>/',approve_post,name="approve_post"),
	path('suggest_changes/<post_id>/',suggest_changes,name="suggest_changes"),
	path('suspend_post/<post_id>/',suspend_post,name="suspend_post"),
	path('users/',users,name="users"),
	path('user_deatail/<id>/',user_deatail,name="user_deatail"),
	path('all-approve-post/',all_approve_post,name="all_approve_post"),
	path('all-unapprove-post/',all_unapprove_post,name="all_unapprove_post"),
	path('all-suspended-post/',all_suspended_post,name="all_suspended_post"),
	path('unapprove/<id>/',unapprove,name="unapprove"),
	path('unsuspend_post/<id>/',unsuspend_post,name="unsuspend_post"),


]
