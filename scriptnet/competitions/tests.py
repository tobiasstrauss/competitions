from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Affiliation, Competition, Individual
from .models import Track, Subtrack

def create_competitions_tracks_subtracks(num_comps, num_tracks_per_comp, num_subtracks_per_track):
    """
    A helper function that creates test competitions, tracks and subtracks.
    Creates a set number of competitions, then the given number of tracks per competition,
    and the given number of subtracks per track.
    """
    for cnum in range(1, num_comps):
        comp = Competition.objects.create(name='Competition {}'.format(cnum))
        for tnum in range(1, num_tracks_per_comp):
            track = Track.objects.create(name='Track {}'.format(tnum))
            for snum in range(1, num_subtracks_per_track):
                subtrack = Subtrack.objects.create(name='Subtrack {}'.format(snum))

class UrlTests(TestCase):
    """
    Check that the regexps in urls.py match to what we should expect
    """
    def test_regexp_index(self):
        a = reverse('index')
        self.assertEqual(a, '/competitions/')        

    def test_regexp_competitions_comp_track_subtrack(self):
        a = reverse('competition', kwargs = { 'competition_id': '1', 'track_id': '1', 'subtrack_id': '1', })
        self.assertEqual(a, '/competitions/1/1/1/')

    def test_regexp_competitions_comp_track(self):
        a = reverse('competition', kwargs = { 'competition_id': '1', 'track_id': '1', })
        self.assertEqual(a, '/competitions/1/1/')

    def test_regexp_competitions_comp(self):
        a = reverse('competition', kwargs = { 'competition_id': '1', })
        self.assertEqual(a, '/competitions/1/')

    def test_regexp_viewresults_comp_track_subtrack(self):
        a = reverse('viewresults', kwargs = {'competition_id': '1', 'track_id': '1', 'subtrack_id': '1',})
        self.assertEqual(a, '/competitions/1/1/1/viewresults/')

    def test_regexp_viewresults_comp_track(self):
        a = reverse('viewresults', kwargs = {'competition_id': '1', 'track_id': '1', })
        self.assertEqual(a, '/competitions/1/1/viewresults/')

    def test_regexp_viewresults_comp(self):
        a = reverse('viewresults', kwargs = {'competition_id': '1', })
        self.assertEqual(a, '/competitions/1/viewresults/')

class ViewForwardTests(TestCase):
    """
    Check that redirections work for various forms of given regexps.
    They should match those found at urls.py
    """
    def test_forward_index(self):
        response = self.client.get('/competitions/')
        self.assertEqual(response.status_code, 200)

    def test_forward_competitions_with_empty_dbase(self):
        response = self.client.get('/competitions/1/1/1/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/competitions/1/1/1')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/competitions/1/1/')
        self.assertEqual(response.status_code, 404)        
        response = self.client.get('/competitions/1/1')
        self.assertEqual(response.status_code, 404)        
        response = self.client.get('/competitions/1/')
        self.assertEqual(response.status_code, 404)        
        response = self.client.get('/competitions/1')
        self.assertEqual(response.status_code, 404)        

    def test_forward_competitions(self):
        create_competitions_tracks_subtracks(1, 1, 1)
        response = self.client.get('/competitions/1/1/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/competitions/1/1/1')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/competitions/1/1/')
        self.assertEqual(response.status_code, 200)        
        response = self.client.get('/competitions/1/1')
        self.assertEqual(response.status_code, 200)        
        response = self.client.get('/competitions/1/')
        self.assertEqual(response.status_code, 200)        
        response = self.client.get('/competitions/1')
        self.assertEqual(response.status_code, 200)        


class ViewReverseTests(TestCase):
    """
    Check that django.core.urlresolvers.reverse works
    for all views that reside in urls.py
    """
    def test_reverse_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_reverse_competition_with_empty_dbase_1(self):
        response = self.client.get(reverse('competition', 
            kwargs={
                'competition_id':'1', 
                'track_id':'1', 
                'subtrack_id':'1',
                }
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_reverse_competition_with_empty_dbase_2(self):
        response = self.client.get(reverse('competition', 
            kwargs={
                'competition_id':'2', 
                'track_id':'3', 
                'subtrack_id':'1',
                }
            )
        )
        self.assertEqual(response.status_code, 404)

class ModelTests(TestCase):
    def test_affiliation_creation(self):
        """
        Create an affiliation and test that it appears
        on the master page -- should reside in one of 
        the buttons of the register block
        """
        testname = 'Test affiliation'
        w = Affiliation.objects.create(name=testname)
        response = self.client.get(reverse('index'))
        self.assertContains(response, testname)

    def test_competition_creation(self):
        """
        Create a competition and test that it appears
        on the master page -- there is a special block 
        that shows all competitions
        """
        testname = 'Test competition'
        w = Competition.objects.create(name=testname)
        response = self.client.get(reverse('index'))
        self.assertContains(response, testname)
    
    def test_track_uniquepercomp_ids(self):
        """
        Check that all track 'unique per competition ids' are indeed unique
        """
        create_competitions_tracks_subtracks(3, 3, 3)
        self.assertEqual(1, 0)

    def test_subtrack_uniquepercomp_ids(self):
        """
        Check that all subtrack 'unique per competition ids' are indeed unique
        """
        create_competitions_tracks_subtracks(2, 2, 5)
        self.assertEqual(1, 0)
        
    def test_user_creation(self):
        """
        Creation of a user should automatically create an 'Individual',
        since Individual is on a 1-1 relationship with User, ie it is
        a 'User profile'.
        """
        testname = 'Test user'
        w = User.objects.create_user(username=testname)
        q = User.objects.get(username=testname)
        self.assertEqual(w, q)
        iq = Individual.objects.all()
        self.assertEqual(len(iq), 1)

class EvaluatorTests(TestCase):
    #TODO: check that all available benchmarks run, and that they give 
    # the results that is expected for a preset dataset.
    def test_evaluator_prwto(self):
        self.assertEqual(1, 1)

class ViewTests(TestCase):
    """
    Tests that check that all views work, after having created
    having populated the dbase with competitions/tracks/subtracks
    """    
    def test_competitionview(self):
        """
        Check that the competitions view should return sth
        when there _are_ registered competitions
        """
        self.assertEqual(1, 1)

    def test_trackview(self):
        """
        Check that the track view should return sth
        when there _are_ tracks in a competition
        """
        self.assertEqual(1, 1)

    def test_subtrackview(self):
        """
        Check that the subtrack view should return sth
        when there _are_ subtracks in a track
        """
        self.assertEqual(1, 1)

class AuthenticationTests(TestCase):
    def test_login_unknown_user(self):
        #Login with an invalid user
        self.assertEqual(1, 1)        

    def test_user_creation_and_login(self):
        """
        Create a user and authenticate him
        """
        self.assertEqual(1, 1)
    
class FormTests(TestCase):
    def test_registerform(self):
        self.assertEqual(1, 1)
    def test_loginform(self):
        self.assertEqual(1, 1)
    def test_submitresultform(self):
        self.assertEqual(1, 1)