from django.test import TestCase
from django.urls import reverse
from rango.models import Comment, UserProfile, User, Category, Friend, LikedCat

class CommentMethodTests(TestCase):

    def test_ensure_comment_has_date_added_field_populated(self):
        '''
        If comment is added, ensure the date_added field is automatically populated
        '''
        #Arrange
        user = add_user("johndoe", "John", "Doe")
        category = add_category("test")
        comment = add_comment_auto_date(user, "This is a Test Comment", category)
        
        #Act

        #Assert
        self.assertIsNotNone(comment.date_added)

class FriendMethodTests(TestCase):
    def test_deletion_of_user_cascade_deletes_friends(self):
        #Arrange
        user_one = add_user("johndoe", "John", "Doe")
        user_two = add_user("janedoe", "Jane", "Doe")
        user_three = add_user("alices", "Alice", "Sender")
        user_four = add_user("bobr", "John", "Reciever")

        userprofile_one = add_user_profile(user_one)
        userprofile_two = add_user_profile(user_two)
        userprofile_three = add_user_profile(user_three)
        userprofile_four = add_user_profile(user_four)

        friend_john = add_friend(userprofile_one, userprofile_two)
        friend_john = add_friend(userprofile_one, userprofile_three)
        friend_john = add_friend(userprofile_one, userprofile_four)

        friend_jane = add_friend(userprofile_two, userprofile_one)
        friend_jane = add_friend(userprofile_two, userprofile_three)

        #Act
        user_one.delete()

        all_users = User.objects.all()
        all_userprofiles = UserProfile.objects.all()
        all_friends = Friend.objects.all()

        #Assert
        self.assertEqual(all_users.count(), 3)
        self.assertEqual(all_userprofiles.count(), 3)
        self.assertEqual(all_friends.count(), 1)
        self.assertEqual(friend_jane.friends.count(), 1)

class LikedCatMethodTests(TestCase):
    def test_deletion_of_user_cascade_deletes_likes(self):
        #Arrange
        user_one = add_user("johndoe", "John", "Doe")
        user_two = add_user("janedoe", "Jane", "Doe")

        userprofile_one = add_user_profile(user_one)
        userprofile_two = add_user_profile(user_two)

        category_one =add_category("Test One")
        category_two =add_category("Test Two")

        likes_john = add_like(userprofile_one, category_one)
        likes_john = add_like(userprofile_one, category_two)

        likes_jane = add_like(userprofile_two, category_one)
        likes_jane = add_like(userprofile_two, category_two)

        #Act
        user_one.delete()
        
        all_users = User.objects.all()
        all_userprofiles = UserProfile.objects.all()
        all_likes = LikedCat.objects.all()

        #Assert
        self.assertEqual(all_users.count(), 1)
        self.assertEqual(all_userprofiles.count(), 1)
        self.assertEqual(all_likes.count(), 1)
        self.assertEqual(likes_jane.likedcats.count(), 2)

class CategoryViewTests(TestCase):

    def test_category_view_with_no_comments(self):
        '''
        If category has no comments, ensure it says "There are no comments yet..." and context comments are empty
        '''
        #Arrange
        category = add_category("test")
        
        #Act
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': category.slug}))

        #Assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no comments yet...")
        self.assertQuerysetEqual(response.context['comments'], [])

    def test_category_view_with_comments(self):
        '''
        If category has comments, ensure it returns in the context
        '''

        #Arrange
        category = add_category("test")
        other_category = add_category("other test")

        user = add_user("johndoe", "John", "Doe")
        user = add_user("janedoe", "Jane", "Doe")

        comment_one = add_comment_auto_date(user, "This is a Test Comment", category)
        comment_two = add_comment_auto_date(user, "This is another Test Comment", category)
        comment_three = add_comment_auto_date(user, "Hey there!", other_category)

        #Act
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': category.slug}))

        #Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['comments'].count(), 2)

class ProfileViewTests(TestCase):
    def test_if_friends_display_on_profile_page(self):

        '''
        If userprofile has friends, display friends on profile page
        '''

        #Arrange
        user_one = add_user("johndoe", "John", "Doe")
        user_two = add_user("janedoe", "Jane", "Doe")
        user_three = add_user("alice", "Alice", "Sender")

        userprofile_one = add_user_profile(user_one)
        userprofile_two = add_user_profile(user_two)
        userprofile_three = add_user_profile(user_three)

        friend = add_friend(userprofile_one, userprofile_two)
        friend = add_friend(userprofile_one, userprofile_three)

        #Act
        response = self.client.get(reverse('rango:profile', kwargs={'username': user_one.username}))

        #Assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "johndoe")
        self.assertContains(response, "janedoe")
        self.assertContains(response, "alice")
        
    def test_if_no_friends_display_on_profile_page(self):

        '''
        If userprofile has no friends, display "No Friends"
        '''

        #Arrange
        user_one = add_user("johndoe", "John", "Doe")
        userprofile_one = add_user_profile(user_one)

        #Act
        response = self.client.get(reverse('rango:profile', kwargs={'username': user_one.username}))
        
        #Assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Friends")

    def test_if_likes_display_on_profile_page(self):
        '''
        If userprofile has likes, display likes on profile page
        '''
        #Arrange
        user_one = add_user("johndoe", "John", "Doe")
        userprofile = add_user_profile(user_one)
        category_one = add_category("Test One")
        category_two = add_category("Test Two")

        like_one = add_like(userprofile, category_one)
        like_two = add_like(userprofile, category_two)

        #Act
        response = self.client.get(reverse('rango:profile', kwargs={'username': user_one.username}))

        #Assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "johndoe")
        self.assertContains(response, "Test One")
        self.assertContains(response, "Test Two")


    def test_if_no_likes_display_on_profile_page(self):
        '''
        If userprofile has no likes, display "No Liked categories"
        '''
        #Arrange
        user_one = add_user("johndoe", "John", "Doe")
        userprofile = add_user_profile(user_one)

        #Act
        response = self.client.get(reverse('rango:profile', kwargs={'username': user_one.username}))

        #Assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "johndoe")
        self.assertContains(response, "No Liked categories")

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

def add_like(userprofile, category):
    liked_cat = LikedCat.objects.get_or_create(user_profile=userprofile)[0]
    liked_cat.likedcats.add(category)
    liked_cat.save()

    return liked_cat