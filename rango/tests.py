from django.test import TestCase
from django.urls import reverse
from rango.models import Comment, UserProfile, User, Category, Friend

class CommentMethodTests(TestCase):

    def test_ensure_comment_has_date_added_field_populated(self):
        '''
        If comment is added, ensure the date_added field is automatically populated
        '''
        user = add_user("johndoe", "John", "Doe")
    
        category = add_category("test")

        comment = add_comment_auto_date(user, "This is a Test Comment", category)

        self.assertIsNotNone(comment.date_added)

class CategoryViewTests(TestCase):

    def test_category_view_with_no_comments(self):
        '''
        If category has no comments, ensure it says "There are no comments yet..." and context comments are empty
        '''
        category = add_category("test")
        
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': category.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no comments yet...")
        self.assertQuerysetEqual(response.context['comments'], [])

    def test_category_view_with_comments(self):
        '''
        If category has comments, ensure it returns in the context
        '''
        category = add_category("test")
        other_category = add_category("other test")

        user = add_user("johndoe", "John", "Doe")
        user = add_user("janedoe", "Jane", "Doe")

        comment_one = add_comment_auto_date(user, "This is a Test Comment", category)
        comment_two = add_comment_auto_date(user, "This is another Test Comment", category)
        comment_three = add_comment_auto_date(user, "Hey there!", other_category)

        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': category.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['comments'].count(), 2)

class ProfileViewTests(TestCase):
    def test_if_friends_display_on_profile_page(self):

        '''
        If userprofile has friends, display friends on profile page
        '''

        user_one = add_user("johndoe", "John", "Doe")
        user_two = add_user("janedoe", "Jane", "Doe")
        user_three = add_user("alice", "Alice", "Sender")

        userprofile_one = add_user_profile(user_one)
        userprofile_two = add_user_profile(user_two)
        userprofile_three = add_user_profile(user_three)

        friend = add_friend(userprofile_one, userprofile_two)
        friend = add_friend(userprofile_one, userprofile_three)

        response = self.client.get(reverse('rango:profile', kwargs={'username': user_one.username}))

        print(response)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "johndoe")
        self.assertContains(response, "janedoe")
        self.assertContains(response, "alice")
        
    def test_if_no_friends_display_on_profile_page(self):

        '''
        If userprofile has no friends, display "No Friends"
        '''

        user_one = add_user("johndoe", "John", "Doe")

        userprofile_one = add_user_profile(user_one)

        response = self.client.get(reverse('rango:profile', kwargs={'username': user_one.username}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Friends")

def add_user(username="johndoe", firstname="John", lastname="Doe"):
    user = User.objects.get_or_create(username=username)[0]
    user.first_name = firstname
    user.last_name = lastname
    user.save()

    return user

def add_category(name, likes=0, views=0):
    category = Category.objects.get_or_create(name=name)[0]
    category.likes=10
    category.views=100
    category.save()

    return category

def add_comment_auto_date(user, text, category):
    comment = Comment.objects.get_or_create(user=user, text=text, category=category)[0]
    comment.save()

    return comment

def add_user_profile(user):
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    userprofile.save()

    return userprofile

def add_friend(userprofile_current, userprofile_to_add):
    friend = Friend.objects.get_or_create(user_profile=userprofile_current)[0]
    friend.friends.add(userprofile_to_add)
    friend.save()

    return friend