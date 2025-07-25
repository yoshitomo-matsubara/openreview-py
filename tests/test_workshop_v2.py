from __future__ import absolute_import, division, print_function, unicode_literals
import openreview
import pytest
import datetime
import time
import os
import re
import random
import csv
from openreview.api import OpenReviewClient
from openreview.api import Note
from openreview.api import Group
from openreview.api import Invitation
from openreview.api import Edge
from selenium.webdriver.common.by import By

from openreview.venue import Venue
from openreview.stages import SubmissionStage, BidStage

class TestWorkshopV2():


    def test_create_conference(self, client, openreview_client, helpers):

        now = datetime.datetime.now()
        due_date = now + datetime.timedelta(days=3)

        # Post the request form note
        helpers.create_user('pc@icaps.cc', 'Program', 'ICAPSChair')
        pc_client = openreview.Client(username='pc@icaps.cc', password=helpers.strong_password)

        helpers.create_user('reviewer1@icaps.cc', 'Reviewer', 'ICAPSOne')
        helpers.create_user('reviewer2@icaps.cc', 'Reviewer', 'ICAPSTwo')
        helpers.create_user('reviewer3@icaps.cc', 'Reviewer', 'ICAPSThree')
        helpers.create_user('reviewer4@icaps.cc', 'Reviewer', 'ICAPSFour')
        helpers.create_user('reviewer5@icaps.cc', 'Reviewer', 'ICAPSFive')
        helpers.create_user('reviewer6@icaps.cc', 'Reviewer', 'ICAPSSix')
        helpers.create_user('external_reviewer1@adobe.com', 'External Reviewer', 'Adobe', institution='adobe.com')

        request_form_note = pc_client.post_note(openreview.Note(
            invitation='openreview.net/Support/-/Request_Form',
            signatures=['~Program_ICAPSChair1'],
            readers=[
                'openreview.net/Support',
                '~Program_ICAPSChair1'
            ],
            writers=[],
            content={
                'title': 'PRL Workshop Series Bridging the Gap Between AI Planning and Reinforcement Learning',
                'Official Venue Name': 'PRL Workshop Series Bridging the Gap Between AI Planning and Reinforcement Learning',
                'Abbreviated Venue Name': 'PRL ICAPS 2023',
                'Official Website URL': 'https://prl-theworkshop.github.io/',
                'program_chair_emails': ['pc@icaps.cc'],
                'contact_email': 'pc@icaps.cc',
                'publication_chairs':'No, our venue does not have Publication Chairs',
                'Area Chairs (Metareviewers)': 'No, our venue does not have Area Chairs',
                'senior_area_chairs': 'No, our venue does not have Senior Area Chairs',
                'Venue Start Date': '2023/07/01',
                'Submission Deadline': due_date.strftime('%Y/%m/%d'),
                'Location': 'Virtual',
                'submission_reviewer_assignment': 'Manual',
                'Author and Reviewer Anonymity': 'Double-blind',
                'reviewer_identity': ['Program Chairs'],
                'area_chair_identity': ['Program Chairs'],
                'senior_area_chair_identity': ['Program Chairs'],
                'Open Reviewing Policy': 'Submissions and reviews should both be private.',
                'submission_readers': 'Program chairs and paper authors only',
                'How did you hear about us?': 'ML conferences',
                'Expected Submissions': '100',
                'use_recruitment_template': 'Yes',
                'api_version': '2',
                'submission_license': ['CC BY 4.0'],
                'venue_organizer_agreement': [
                    'OpenReview natively supports a wide variety of reviewing workflow configurations. However, if we want significant reviewing process customizations or experiments, we will detail these requests to the OpenReview staff at least three months in advance.',
                    'We will ask authors and reviewers to create an OpenReview Profile at least two weeks in advance of the paper submission deadlines.',
                    'When assembling our group of reviewers and meta-reviewers, we will only include email addresses or OpenReview Profile IDs of people we know to have authored publications relevant to our venue.  (We will not solicit new reviewers using an open web form, because unfortunately some malicious actors sometimes try to create "fake ids" aiming to be assigned to review their own paper submissions.)',
                    'We acknowledge that, if our venue\'s reviewing workflow is non-standard, or if our venue is expecting more than a few hundred submissions for any one deadline, we should designate our own Workflow Chair, who will read the OpenReview documentation and manage our workflow configurations throughout the reviewing process.',
                    'We acknowledge that OpenReview staff work Monday-Friday during standard business hours US Eastern time, and we cannot expect support responses outside those times.  For this reason, we recommend setting submission and reviewing deadlines Monday through Thursday.',
                    'We will treat the OpenReview staff with kindness and consideration.'
                ]
            }))

        helpers.await_queue()

        # Post a deploy note
        client.post_note(openreview.Note(
            content={'venue_id': 'PRL/2023/ICAPS'},
            forum=request_form_note.forum,
            invitation='openreview.net/Support/-/Request{}/Deploy'.format(request_form_note.number),
            readers=['openreview.net/Support'],
            referent=request_form_note.forum,
            replyto=request_form_note.forum,
            signatures=['openreview.net/Support'],
            writers=['openreview.net/Support']
        ))

        helpers.await_queue()

        assert openreview_client.get_group('PRL/2023/ICAPS')
        assert openreview_client.get_group('PRL/2023/ICAPS/Program_Chairs')
        
        with pytest.raises(openreview.OpenReviewException, match=r'Group Not Found: PRL/2023/ICAPS/Senior_Area_Chairs'):
            assert openreview_client.get_group('PRL/2023/ICAPS/Senior_Area_Chairs')
        with pytest.raises(openreview.OpenReviewException, match=r'Group Not Found: PRL/2023/ICAPS/Area_Chairs'):
            assert openreview_client.get_group('PRL/2023/ICAPS/Area_Chairs')
        
        assert openreview_client.get_group('PRL/2023/ICAPS/Reviewers')
        assert openreview_client.get_group('PRL/2023/ICAPS/Authors')

        submission_invitation = openreview_client.get_invitation('PRL/2023/ICAPS/-/Submission')
        assert submission_invitation
        assert submission_invitation.duedate

        # assert openreview_client.get_invitation('PRL/2023/ICAPS/Reviewers/-/Expertise_Selection')
        with pytest.raises(openreview.OpenReviewException, match=r'The Invitation PRL/2023/ICAPS/Area_Chairs/-/Expertise_Selection was not found'):
            assert openreview_client.get_invitation('PRL/2023/ICAPS/Area_Chairs/-/Expertise_Selection')
        with pytest.raises(openreview.OpenReviewException, match=r'The Invitation PRL/2023/ICAPS/Senior_Area_Chairs/-/Expertise_Selection was not found'):
            assert openreview_client.get_invitation('PRL/2023/ICAPS/Senior_Area_Chairs/-/Expertise_Selection')

    def test_submissions(self, client, openreview_client, helpers, test_client):

        test_client = openreview.api.OpenReviewClient(token=test_client.token)
        pc_client=openreview.Client(username='pc@icaps.cc', password=helpers.strong_password)
        pc_client_v2=openreview.api.OpenReviewClient(username='pc@icaps.cc', password=helpers.strong_password)
        request_form=pc_client.get_notes(invitation='openreview.net/Support/-/Request_Form')[0]

        domains = ['umass.edu', 'amazon.com', 'fb.com', 'cs.umass.edu', 'google.com', 'mit.edu', 'deepmind.com', 'co.ux', 'apple.com', 'nvidia.com']
        for i in range(1,12):
            note = openreview.api.Note(
                content = {
                    'title': { 'value': 'Paper title ' + str(i) },
                    'abstract': { 'value': 'This is an abstract ' + str(i) },
                    'authorids': { 'value': ['~SomeFirstName_User1', 'peter@mail.com', 'andrew@' + domains[i % 10]] },
                    'authors': { 'value': ['SomeFirstName User', 'Peter SomeLastName', 'Andrew Mc'] },
                    'keywords': { 'value': ['machine learning', 'nlp'] },
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                }
            )
            
            test_client.post_note_edit(invitation='PRL/2023/ICAPS/-/Submission',
                signatures=['~SomeFirstName_User1'],
                note=note)

        # Post revision to remove abstract from submission form
        now = datetime.datetime.now()
        due_date = now + datetime.timedelta(days=3)

        pc_client.post_note(openreview.Note(
            content={
                'title': 'PRL Workshop Series Bridging the Gap Between AI Planning and Reinforcement Learning',
                'Official Venue Name': 'PRL Workshop Series Bridging the Gap Between AI Planning and Reinforcement Learning',
                'Abbreviated Venue Name': 'PRL ICAPS 2023',
                'Official Website URL': 'https://prl-theworkshop.github.io/',
                'program_chair_emails': ['pc@icaps.cc'],
                'contact_email': 'pc@icaps.cc',
                'publication_chairs':'No, our venue does not have Publication Chairs',
                'Venue Start Date': '2023/07/01',
                'Submission Deadline': due_date.strftime('%Y/%m/%d'),
                'Location': 'Virtual',
                'submission_reviewer_assignment': 'Manual',
                'How did you hear about us?': 'ML conferences',
                'Expected Submissions': '100',
                'use_recruitment_template': 'Yes',
                'remove_submission_options': ['abstract']

            },
            forum=request_form.forum,
            invitation='openreview.net/Support/-/Request{}/Revision'.format(request_form.number),
            readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
            referent=request_form.forum,
            replyto=request_form.forum,
            signatures=['~Program_ICAPSChair1'],
            writers=[]
        ))

        helpers.await_queue()
        
        # Post submission with no abstract
        note = openreview.api.Note(
            content = {
                'title': { 'value': 'Paper title No Abstract' },
                'authorids': { 'value': ['~SomeFirstName_User1', 'peter@mail.com', 'andrew@' + 'umass.edu'] },
                'authors': { 'value': ['SomeFirstName User', 'Peter SomeLastName', 'Andrew Mc'] },
                'keywords': { 'value': ['machine learning', 'nlp'] },
                'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
            }
        )
        
        test_client.post_note_edit(invitation='PRL/2023/ICAPS/-/Submission',
            signatures=['~SomeFirstName_User1'],
            note=note)

        helpers.await_queue_edit(openreview_client, invitation='PRL/2023/ICAPS/-/Submission', count=12)

        submissions = openreview_client.get_notes(invitation='PRL/2023/ICAPS/-/Submission', sort='number:asc')
        assert len(submissions) == 12
        assert ['PRL/2023/ICAPS', '~SomeFirstName_User1', 'peter@mail.com', 'andrew@amazon.com'] == submissions[0].readers
        assert ['~SomeFirstName_User1', 'peter@mail.com', 'andrew@amazon.com'] == submissions[0].content['authorids']['value']

        authors_group = openreview_client.get_group(id='PRL/2023/ICAPS/Authors')

        for i in range(1,13):
            assert f'PRL/2023/ICAPS/Submission{i}/Authors' in authors_group.members

        # PC Revision of submission with no abstract
        submission = submissions[11]
        edit_note = pc_client_v2.post_note_edit(invitation='PRL/2023/ICAPS/-/PC_Revision',
            signatures=['PRL/2023/ICAPS/Program_Chairs'],
            note=openreview.api.Note(
                id = submission.id,
                content = {
                    'title': { 'value': submission.content['title']['value'] + ' Version 2' },
                    'authorids': { 'value': submission.content['authorids']['value']},
                    'authors': { 'value': submission.content['authors']['value']},
                    'keywords': submission.content['keywords'],
                    'pdf': submission.content['pdf'],
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=edit_note['id'])
                                                                                    
        messages = openreview_client.get_messages(to='peter@mail.com', subject='PRL ICAPS 2023 has received a new revision of your submission titled Paper title No Abstract Version 2')
        assert messages and len(messages) == 1
        # Test that abstract doesn't appear in PC Revision email
        assert messages[0]['content']['text'].startswith('Your new revision of the submission to PRL ICAPS 2023 has been posted.\n\nTitle: Paper title No Abstract Version 2\n\nTo view your submission, click here:')

    def test_setup_matching(self, client, openreview_client, helpers):

        pc_client=openreview.Client(username='pc@icaps.cc', password=helpers.strong_password)
        pc_client_v2=openreview.api.OpenReviewClient(username='pc@icaps.cc', password=helpers.strong_password)
        request_form=pc_client.get_notes(invitation='openreview.net/Support/-/Request_Form')[0]

        submissions = pc_client_v2.get_notes(invitation='PRL/2023/ICAPS/-/Submission', sort='number:asc')
        pc_client_v2.add_members_to_group('PRL/2023/ICAPS/Reviewers', ['reviewer1@icaps.cc', 'reviewer2@icaps.cc', 'reviewer3@icaps.cc', 'reviewer4@icaps.cc', 'reviewer5@icaps.cc', 'reviewer6@icaps.cc'])

        openreview.tools.replace_members_with_ids(openreview_client, openreview_client.get_group('PRL/2023/ICAPS/Reviewers'))
        
        with open(os.path.join(os.path.dirname(__file__), 'data/rev_scores_venue.csv'), 'w') as file_handle:
            writer = csv.writer(file_handle)
            for submission in submissions:
                for ac in openreview_client.get_group('PRL/2023/ICAPS/Reviewers').members:
                    writer.writerow([submission.id, ac, round(random.random(), 2)])

        affinity_scores_url = client.put_attachment(os.path.join(os.path.dirname(__file__), 'data/rev_scores_venue.csv'), f'openreview.net/Support/-/Request{request_form.number}/Paper_Matching_Setup', 'upload_affinity_scores')

        ## setup matching data before starting bidding
        client.post_note(openreview.Note(
            content={
                'title': 'Paper Matching Setup',
                'matching_group': 'PRL/2023/ICAPS/Reviewers',
                'compute_conflicts': 'Default',
                'compute_affinity_scores': 'No',
                'upload_affinity_scores': affinity_scores_url

            },
            forum=request_form.id,
            replyto=request_form.id,
            invitation=f'openreview.net/Support/-/Request{request_form.number}/Paper_Matching_Setup',
            readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
            signatures=['~Program_ICAPSChair1'],
            writers=[]
        ))
        helpers.await_queue()

        assert pc_client_v2.get_edges_count(invitation='PRL/2023/ICAPS/Reviewers/-/Affinity_Score') == 72

        with pytest.raises(openreview.OpenReviewException, match=r'The Invitation PRL/2023/ICAPS/Reviewers/-/Proposed_Assignment was not found'):
            assert openreview_client.get_invitation('PRL/2023/ICAPS/Reviewers/-/Proposed_Assignment')

        with pytest.raises(openreview.OpenReviewException, match=r'The Invitation PRL/2023/ICAPS/Reviewers/-/Aggregate_Score was not found'):
            assert openreview_client.get_invitation('PRL/2023/ICAPS/Reviewers/-/Aggregate_Score')

        assert openreview_client.get_invitation('PRL/2023/ICAPS/Reviewers/-/Assignment')                    
        assert openreview_client.get_invitation('PRL/2023/ICAPS/Reviewers/-/Custom_Max_Papers')                    
        assert openreview_client.get_invitation('PRL/2023/ICAPS/Reviewers/-/Custom_User_Demands')

        ## try to make an assignment and get an error because the submission deadline has not passed
        with pytest.raises(openreview.OpenReviewException, match=r'Can not make assignment, submission Reviewers group not found.'):
            edge = pc_client_v2.post_edge(openreview.api.Edge(
                invitation='PRL/2023/ICAPS/Reviewers/-/Assignment',
                head=submissions[0].id,
                tail='~Reviewer_ICAPSOne1',
                weight=1,
                signatures=['PRL/2023/ICAPS/Program_Chairs']
            ))

        ## close the submission
        now = datetime.datetime.now()
        start_date = now - datetime.timedelta(days=2)
        due_date = now - datetime.timedelta(hours=1)        
        pc_client.post_note(openreview.Note(
            content={
                'title': 'PRL Workshop Series Bridging the Gap Between AI Planning and Reinforcement Learning',
                'Official Venue Name': 'PRL Workshop Series Bridging the Gap Between AI Planning and Reinforcement Learning',
                'Abbreviated Venue Name': 'PRL ICAPS 2023',
                'Official Website URL': 'https://prl-theworkshop.github.io/',
                'program_chair_emails': ['pc@icaps.cc'],
                'contact_email': 'pc@icaps.cc',
                'publication_chairs':'No, our venue does not have Publication Chairs',
                'Venue Start Date': '2023/07/01',
                'Submission Deadline': due_date.strftime('%Y/%m/%d %H:%M'),
                'Submission Start Date': start_date.strftime('%Y/%m/%d %H:%M'),
                'Location': 'Virtual',
                'submission_reviewer_assignment': 'Manual',
                'How did you hear about us?': 'ML conferences',
                'Expected Submissions': '100',
                'use_recruitment_template': 'Yes'

            },
            forum=request_form.forum,
            invitation='openreview.net/Support/-/Request{}/Revision'.format(request_form.number),
            readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
            referent=request_form.forum,
            replyto=request_form.forum,
            signatures=['~Program_ICAPSChair1'],
            writers=[]
        ))

        helpers.await_queue()

        for submission in submissions:
            edge = pc_client_v2.post_edge(openreview.api.Edge(
                invitation='PRL/2023/ICAPS/Reviewers/-/Assignment',
                head=submission.id,
                tail='~Reviewer_ICAPSOne1',
                weight=1,
                signatures=['PRL/2023/ICAPS/Program_Chairs']
            ))

            helpers.await_queue_edit(openreview_client, edit_id=edge.id)

        assert openreview_client.get_group('PRL/2023/ICAPS/Submission1/Reviewers').members == ['~Reviewer_ICAPSOne1']

        # Invite external reviewer to submission with no abstract
        conference = openreview.helpers.get_conference(client, request_form.id)
        conference.setup_assignment_recruitment(conference.get_reviewers_id(), '12345678', now + datetime.timedelta(days=3), invitation_labels={ 'Invite': 'Invitation Sent', 'Invited': 'Invitation Sent' })
        
        submission = submissions[11]
        edge = pc_client_v2.post_edge(openreview.api.Edge(
            invitation='PRL/2023/ICAPS/Reviewers/-/Invite_Assignment',
            readers = ['PRL/2023/ICAPS', 'external_reviewer1@adobe.com'],
            nonreaders = ['PRL/2023/ICAPS/Submission12/Authors'],
            writers = [conference.id],
            signatures = ['PRL/2023/ICAPS/Program_Chairs'],
            head = submission.id,
            tail = 'external_reviewer1@adobe.com',
            label = 'Invitation Sent',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=edge.id)

        messages = openreview_client.get_messages(to='external_reviewer1@adobe.com', subject='[PRL ICAPS 2023] Invitation to review paper titled "Paper title No Abstract Version 2"')
        assert messages and len(messages) == 1
        # Test that abstract doesn't appear in Invite Assignment email
        assert messages[0]['content']['text'].startswith('Hi External Reviewer Adobe,\n\nYou were invited to review the paper number: 12, title: "Paper title No Abstract Version 2".\n\nPlease respond the invitation clicking the following link:')
        assert messages[0]['content']['replyTo'] == 'pc@icaps.cc'

    def test_review_stage(self, client, openreview_client, helpers, request_page, selenium):


        pc_client=openreview.Client(username='pc@icaps.cc', password=helpers.strong_password)
        pc_client_v2=openreview.api.OpenReviewClient(username='pc@icaps.cc', password=helpers.strong_password)
        request_form=pc_client.get_notes(invitation='openreview.net/Support/-/Request_Form')[0]

        pc_client.post_note(openreview.Note(
            content= {
                'force': 'Yes',
                'submission_readers': 'Assigned program committee (assigned reviewers, assigned area chairs, assigned senior area chairs if applicable)'
            },
            forum= request_form.id,
            invitation= f'openreview.net/Support/-/Request{request_form.number}/Post_Submission',
            readers= ['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
            referent= request_form.id,
            replyto= request_form.id,
            signatures= ['~Program_ICAPSChair1'],
            writers= [],
        ))

        helpers.await_queue()

        helpers.await_queue_edit(openreview_client, 'PRL/2023/ICAPS/-/Post_Submission-0-1', count=2)        

        now = datetime.datetime.now()
        start_date = now - datetime.timedelta(days=2)
        due_date = now + datetime.timedelta(days=3)

        # review stage
        review_stage_note=pc_client.post_note(openreview.Note(
            content={
                'review_start_date': start_date.strftime('%Y/%m/%d'),
                'review_deadline': due_date.strftime('%Y/%m/%d'),
                'make_reviews_public': 'No, reviews should NOT be revealed publicly when they are posted',
                'release_reviews_to_authors': 'No, reviews should NOT be revealed when they are posted to the paper\'s authors',
                'release_reviews_to_reviewers': 'Review should not be revealed to any reviewer, except to the author of the review',
                'email_program_chairs_about_reviews': 'No, do not email program chairs about received reviews',
            },
            forum=request_form.forum,
            invitation='openreview.net/Support/-/Request{}/Review_Stage'.format(request_form.number),
            readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
            replyto=request_form.forum,
            referent=request_form.forum,
            signatures=['~Program_ICAPSChair1'],
            writers=[]
        ))
        helpers.await_queue()

        helpers.await_queue_edit(openreview_client, 'PRL/2023/ICAPS/-/Official_Review-0-1', count=1)

        reviewer_client = openreview.api.OpenReviewClient(username='reviewer1@icaps.cc', password=helpers.strong_password)

        submissions = pc_client_v2.get_notes(invitation='PRL/2023/ICAPS/-/Submission', sort='number:asc')

        for submission in submissions:
            anon_groups = reviewer_client.get_groups(prefix=f'PRL/2023/ICAPS/Submission{submission.number}/Reviewer_')
            assert len(anon_groups) == 1

            edit = reviewer_client.post_note_edit(invitation=f'PRL/2023/ICAPS/Submission{submission.number}/-/Official_Review',
                signatures=[anon_groups[0].id],
                note=openreview.api.Note(
                    content={
                        'title': { 'value': 'This is a review for submission 1' },
                        'rating': { 'value': 5 },
                        'review': { 'value': 'This is a review for submission 1' },
                        'confidence': { 'value': 5 },
                    }
                ))
            
            helpers.await_queue_edit(openreview_client, edit_id=edit['id'])
    
    
    def test_publication_chair(self, client, openreview_client, helpers, request_page, selenium):

        pc_client=openreview.Client(username='pc@icaps.cc', password=helpers.strong_password)
        pc_client_v2=openreview.api.OpenReviewClient(username='pc@icaps.cc', password=helpers.strong_password)
        request_form=pc_client.get_notes(invitation='openreview.net/Support/-/Request_Form')[0]

        # Post a decision stage note
        now = datetime.datetime.now()
        start_date = now - datetime.timedelta(days=2)
        due_date = now + datetime.timedelta(days=3)

        with pytest.raises(openreview.OpenReviewException, match=r'Please specify the accept options in "Accept Decision Options"'):
            decision_stage_note = pc_client.post_note(openreview.Note(
                content={
                    'decision_start_date': start_date.strftime('%Y/%m/%d'),
                    'decision_deadline': due_date.strftime('%Y/%m/%d'),
                    'decision_options': 'Invite to Venue, Reject',
                    'make_decisions_public': 'No, decisions should NOT be revealed publicly when they are posted',
                    'release_decisions_to_authors': 'No, decisions should NOT be revealed when they are posted to the paper\'s authors',
                    'release_decisions_to_reviewers': 'No, decisions should not be immediately revealed to the paper\'s reviewers',
                    'release_decisions_to_area_chairs': 'No, decisions should not be immediately revealed to the paper\'s area chairs',
                    'notify_authors': 'Yes, send an email notification to the authors'
                },
                forum=request_form.forum,
                invitation=f'openreview.net/Support/-/Request{request_form.number}/Decision_Stage',
                readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
                referent=request_form.forum,
                replyto=request_form.forum,
                signatures=['~Program_ICAPSChair1'],
                writers=[]
            ))

        with pytest.raises(openreview.OpenReviewException, match=r'All accept decision options must be included in "Decision Options"'):
            decision_stage_note = pc_client.post_note(openreview.Note(
                content={
                    'decision_start_date': start_date.strftime('%Y/%m/%d'),
                    'decision_deadline': due_date.strftime('%Y/%m/%d'),
                    'decision_options': 'Invite to Venue, Reject',
                    'accept_decision_options': 'Invite to Conference',
                    'make_decisions_public': 'No, decisions should NOT be revealed publicly when they are posted',
                    'release_decisions_to_authors': 'No, decisions should NOT be revealed when they are posted to the paper\'s authors',
                    'release_decisions_to_reviewers': 'No, decisions should not be immediately revealed to the paper\'s reviewers',
                    'release_decisions_to_area_chairs': 'No, decisions should not be immediately revealed to the paper\'s area chairs',
                    'notify_authors': 'Yes, send an email notification to the authors'
                },
                forum=request_form.forum,
                invitation=f'openreview.net/Support/-/Request{request_form.number}/Decision_Stage',
                readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
                referent=request_form.forum,
                replyto=request_form.forum,
                signatures=['~Program_ICAPSChair1'],
                writers=[]
            ))
        
        decision_stage_note = pc_client.post_note(openreview.Note(
            content={
                'decision_start_date': start_date.strftime('%Y/%m/%d'),
                'decision_deadline': due_date.strftime('%Y/%m/%d'),
                'decision_options': 'Accept, Invite to Venue, Reject',
                'accept_decision_options': 'Accept, Invite to Venue',
                'make_decisions_public': 'No, decisions should NOT be revealed publicly when they are posted',
                'release_decisions_to_authors': 'No, decisions should NOT be revealed when they are posted to the paper\'s authors',
                'release_decisions_to_reviewers': 'No, decisions should not be immediately revealed to the paper\'s reviewers',
                'release_decisions_to_area_chairs': 'No, decisions should not be immediately revealed to the paper\'s area chairs',
                'notify_authors': 'Yes, send an email notification to the authors'
            },
            forum=request_form.forum,
            invitation=f'openreview.net/Support/-/Request{request_form.number}/Decision_Stage',
            readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
            referent=request_form.forum,
            replyto=request_form.forum,
            signatures=['~Program_ICAPSChair1'],
            writers=[]
        ))
        assert decision_stage_note
        helpers.await_queue()

        helpers.await_queue_edit(openreview_client, 'PRL/2023/ICAPS/-/Decision-0-1', count=1)

        process_logs = client.get_process_logs(id = decision_stage_note.id)
        assert len(process_logs) == 1
        assert process_logs[0]['status'] == 'ok'    

        submissions = openreview_client.get_notes(invitation='PRL/2023/ICAPS/-/Submission', sort='number:asc')
        assert len(submissions) == 12

        decisions = ['Accept', 'Invite to Venue', 'Reject']
        for idx in range(len(submissions[:10])):
            decision = pc_client_v2.post_note_edit(
                invitation=f'PRL/2023/ICAPS/Submission{submissions[idx].number}/-/Decision',
                    signatures=['PRL/2023/ICAPS/Program_Chairs'],
                    note=openreview.api.Note(
                        content={
                            'decision': { 'value': decisions[idx%3] },
                            'comment': { 'value': 'Comment by PCs.' }
                        }
                    )
                )
            
            helpers.await_queue_edit(openreview_client, edit_id=decision['id'])

        invitation = client.get_invitation(f'openreview.net/Support/-/Request{request_form.number}/Post_Decision_Stage')
        invitation.cdate = openreview.tools.datetime_millis(datetime.datetime.now())
        client.post_invitation(invitation)

        # add publication chairs
        pc_client.post_note(openreview.Note(
            content={
                'title': 'PRL Workshop Series Bridging the Gap Between AI Planning and Reinforcement Learning',
                'Official Venue Name': 'PRL Workshop Series Bridging the Gap Between AI Planning and Reinforcement Learning',
                'Abbreviated Venue Name': 'PRL ICAPS 2023',
                'Official Website URL': 'https://prl-theworkshop.github.io/',
                'program_chair_emails': ['pc@icaps.cc'],
                'publication_chairs': 'Yes, our venue has Publication Chairs',
                'publication_chairs_emails': ['publicationchair@mail.com', 'publicationchair2@mail.com'],
                'contact_email': 'pc@icaps.cc',
                'Venue Start Date': '2023/07/01',
                'Submission Deadline': request_form.content['Submission Deadline'],
                'Location': 'Virtual',
                'submission_reviewer_assignment': 'Manual',
                'How did you hear about us?': 'ML conferences',
                'Expected Submissions': '100',
                'use_recruitment_template': 'Yes'

            },
            forum=request_form.forum,
            invitation='openreview.net/Support/-/Request{}/Revision'.format(request_form.number),
            readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
            referent=request_form.forum,
            replyto=request_form.forum,
            signatures=['~Program_ICAPSChair1'],
            writers=[]
        ))

        helpers.await_queue()

        group = openreview_client.get_group('PRL/2023/ICAPS/Publication_Chairs')
        assert group
        assert 'publicationchair@mail.com' in group.members
        assert 'publicationchair2@mail.com' in group.members
        submission_revision_inv = client.get_invitation(f'openreview.net/Support/-/Request{request_form.number}/Submission_Revision_Stage')
        assert 'PRL/2023/ICAPS/Publication_Chairs' in submission_revision_inv.invitees

        #Post a post decision note, release accepted papers to publication chair
        now = datetime.datetime.now()
        start_date = now - datetime.timedelta(days=2)
        due_date = now + datetime.timedelta(days=3)
        short_name = 'PRL ICAPS 2023'
        post_decision_stage_note = pc_client.post_note(openreview.Note(
            content={
                'reveal_authors': 'No, I don\'t want to reveal any author identities.',
                'submission_readers': 'All program committee (all reviewers, all area chairs, all senior area chairs if applicable)',
                'home_page_tab_names': {
                    'Accept': 'Accept',
                    'Invite to Venue': 'Invite to Venue',
                    'Reject': 'Submitted'
                },
                'send_decision_notifications': 'Yes, send an email notification to the authors',
                'accept_email_content': f'''Dear {{{{fullname}}}},

Thank you for submitting your paper, {{{{submission_title}}}}, to {short_name}. We are delighted to inform you that your submission has been accepted. Congratulations!
You can find the final reviews for your paper on the submission page in OpenReview at: {{{{forum_url}}}}

Best,
{short_name} Program Chairs
''',
                'invite_to_venue_email_content': f'''Dear {{{{fullname}}}},

Thank you for submitting your paper, {{{{submission_title}}}}, to {short_name}. We are delighted to inform you that your submission has been invited to the venue. Congratulations!
You can find the final reviews for your paper on the submission page in OpenReview at: {{{{forum_url}}}}

Best,
{short_name} Program Chairs
''',
                'reject_email_content': f'''Dear {{{{fullname}}}},

Thank you for submitting your paper, {{{{submission_title}}}}, to {short_name}. We regret to inform you that your submission was not accepted.
You can find the final reviews for your paper on the submission page in OpenReview at: {{{{forum_url}}}}

Best,
{short_name} Program Chairs
'''
            },
            forum=request_form.forum,
            invitation=invitation.id,
            readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
            replyto=request_form.forum,
            referent=request_form.forum,
            signatures=['~Program_ICAPSChair1'],
            writers=[]
        ))
        assert post_decision_stage_note
        helpers.await_queue()

        submissions = openreview_client.get_notes(invitation='PRL/2023/ICAPS/-/Submission', sort='number:asc')
        assert len(submissions) == 12

        for idx in range(len(submissions[:10])):
            if idx % 3 <= 1:
                assert submissions[idx].readers == [
                    'PRL/2023/ICAPS',
                    'PRL/2023/ICAPS/Reviewers',
                    'PRL/2023/ICAPS/Publication_Chairs',
                    f'PRL/2023/ICAPS/Submission{submissions[idx].number}/Authors'
                ]
                assert submissions[idx].content['authors']['readers'] == [
                    'PRL/2023/ICAPS',
                    f'PRL/2023/ICAPS/Submission{submissions[idx].number}/Authors',
                    'PRL/2023/ICAPS/Publication_Chairs'
                ]
                assert submissions[idx].content['venueid']['value'] == 'PRL/2023/ICAPS'
                submission_venue = 'PRL ICAPS 2023' if idx % 3 == 0 else 'PRL ICAPS 2023 InvitetoVenue'
                assert submissions[idx].content['venue']['value'] == submission_venue
            else:
                assert submissions[idx].readers == [
                    'PRL/2023/ICAPS',
                    'PRL/2023/ICAPS/Reviewers',
                    f'PRL/2023/ICAPS/Submission{submissions[idx].number}/Authors'
                ]
                assert submissions[idx].content['authors']['readers'] == [
                    'PRL/2023/ICAPS',
                    f'PRL/2023/ICAPS/Submission{submissions[idx].number}/Authors'
                ]
                assert submissions[idx].content['venueid']['value'] == 'PRL/2023/ICAPS/Rejected_Submission'
                assert submissions[idx].content['venue']['value'] == 'Submitted to PRL ICAPS 2023'

        assert submissions[10].content['venueid']['value'] == 'PRL/2023/ICAPS/Submission'
        assert submissions[10].content['venue']['value'] == 'PRL 2023 ICAPS Submission'
        assert submissions[10].readers == [
            'PRL/2023/ICAPS',
            'PRL/2023/ICAPS/Submission11/Reviewers',
            'PRL/2023/ICAPS/Submission11/Authors'
        ]
        assert submissions[10].content['authors']['readers'] == [
            'PRL/2023/ICAPS',
            'PRL/2023/ICAPS/Submission11/Authors'
        ]        
        assert submissions[11].content['venueid']['value'] == 'PRL/2023/ICAPS/Submission'
        assert submissions[11].content['venue']['value'] == 'PRL 2023 ICAPS Submission'
        assert submissions[11].readers == [
            'PRL/2023/ICAPS',
            'PRL/2023/ICAPS/Submission12/Reviewers',
            'PRL/2023/ICAPS/Submission12/Authors'
        ]
        assert submissions[11].content['authors']['readers'] == [
            'PRL/2023/ICAPS',
            'PRL/2023/ICAPS/Submission12/Authors'
        ]

        helpers.create_user('publicationchair@mail.com', 'Publication', 'ICAPSChair')
        publication_chair_client_v2=openreview.api.OpenReviewClient(username='publicationchair@mail.com', password=helpers.strong_password)

        assert publication_chair_client_v2.get_group('PRL/2023/ICAPS/Authors/Accepted')
        submissions = publication_chair_client_v2.get_notes(invitation='PRL/2023/ICAPS/-/Submission', sort='number:asc')
        assert len(submissions) == 7

        # Check messages
        messages = openreview_client.get_messages(subject=f'[PRL ICAPS 2023] Decision notification for your submission 1:.*')
        assert len(messages) == 3
        assert 'We are delighted to inform you that your submission has been accepted.' in messages[0]['content']['text']

        messages = openreview_client.get_messages(subject=f'[PRL ICAPS 2023] Decision notification for your submission 2:.*')
        assert 'We are delighted to inform you that your submission has been invited to the venue.' in messages[0]['content']['text']

        messages = openreview_client.get_messages(subject=f'[PRL ICAPS 2023] Decision notification for your submission 3:.*')
        assert 'We regret to inform you that your submission was not accepted.' in messages[0]['content']['text']

        messages = openreview_client.get_messages(subject=f'[PRL ICAPS 2023] Decision notification for your submission 11:.*')
        assert len(messages) == 0

        messages = openreview_client.get_messages(subject=f'[PRL ICAPS 2023] Decision notification for your submission 12:.*')
        assert len(messages) == 0

        # Check homepage tabs
        url = 'http://localhost:3030/group?id=PRL/2023/ICAPS'
        request_page(selenium, f'{url}', token=openreview_client.token, wait_for_element='header')
        tabs = selenium.find_element(By.CLASS_NAME, 'nav-tabs').find_elements(By.TAG_NAME, 'li')
        assert len(tabs) == 4
        assert tabs[0].text == 'Accept'
        assert tabs[1].text == 'Invite to Venue'
        assert tabs[2].text == 'Submitted'
        assert tabs[3].text == 'Recent Activity'

        notes = selenium.find_element(By.ID, 'accept').find_elements(By.CLASS_NAME, 'note')
        assert len(notes) == 4
        assert notes[0].find_element(By.TAG_NAME, 'h4').text == 'Paper title 10'

        request_page(selenium, f'{url}#tab-invite-to-venue', token=openreview_client.token, wait_for_element='header')
        notes = selenium.find_element(By.ID, 'invite-to-venue').find_elements(By.CLASS_NAME, 'note')
        assert len(notes) == 3
        assert notes[0].find_element(By.TAG_NAME, 'h4').text == 'Paper title 8'

        request_page(selenium, f'{url}#tab-submitted', token=openreview_client.token, wait_for_element='header')
        notes = selenium.find_element(By.ID, 'submitted').find_elements(By.CLASS_NAME, 'note')
        assert len(notes) == 3
        assert notes[0].find_element(By.TAG_NAME, 'h4').text == 'Paper title 9'


        decision = openreview_client.get_notes(invitation='PRL/2023/ICAPS/Submission1/-/Decision')[0]
        assert decision.content['decision']['value'] == 'Accept'
        assert decision.content['comment']['value'] == 'Comment by PCs.'
        assert decision.readers == [
            'PRL/2023/ICAPS/Program_Chairs'
        ]

    def test_release_decisions_to_authors(self, client, openreview_client, helpers, selenium, request_page):

        pc_client=openreview.Client(username='pc@icaps.cc', password=helpers.strong_password)
        pc_client_v2=openreview.api.OpenReviewClient(username='pc@icaps.cc', password=helpers.strong_password)
        request_form=pc_client.get_notes(invitation='openreview.net/Support/-/Request_Form')[0]

        # Post a decision stage note
        now = datetime.datetime.now()
        start_date = now - datetime.timedelta(days=2)
        due_date = now + datetime.timedelta(days=3)

        decision_stage_note = pc_client.post_note(openreview.Note(
            content={
                'decision_start_date': start_date.strftime('%Y/%m/%d'),
                'decision_deadline': due_date.strftime('%Y/%m/%d'),
                'decision_options': 'Accept, Invite to Venue, Reject',
                'accept_decision_options': 'Accept, Invite to Venue',
                'make_decisions_public': 'No, decisions should NOT be revealed publicly when they are posted',
                'release_decisions_to_authors': 'Yes, decisions should be revealed when they are posted to the paper\'s authors',
                'release_decisions_to_reviewers': 'No, decisions should not be immediately revealed to the paper\'s reviewers',
                'release_decisions_to_area_chairs': 'No, decisions should not be immediately revealed to the paper\'s area chairs',
                'notify_authors': 'Yes, send an email notification to the authors'
            },
            forum=request_form.forum,
            invitation=f'openreview.net/Support/-/Request{request_form.number}/Decision_Stage',
            readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
            referent=request_form.forum,
            replyto=request_form.forum,
            signatures=['~Program_ICAPSChair1'],
            writers=[]
        ))
        assert decision_stage_note
        helpers.await_queue()

        helpers.await_queue_edit(openreview_client, 'PRL/2023/ICAPS/-/Decision-0-1', count=2)

        decision = openreview_client.get_notes(invitation='PRL/2023/ICAPS/Submission1/-/Decision')[0]
        assert decision.content['decision']['value'] == 'Accept'
        assert decision.content['comment']['value'] == 'Comment by PCs.'
        assert decision.readers == [
            'PRL/2023/ICAPS/Program_Chairs',
            'PRL/2023/ICAPS/Submission1/Authors',
        ]        
    
    def test_release_reviews(self, client, openreview_client, helpers, request_page, selenium):


        pc_client=openreview.Client(username='pc@icaps.cc', password=helpers.strong_password)
        pc_client_v2=openreview.api.OpenReviewClient(username='pc@icaps.cc', password=helpers.strong_password)
        request_form=pc_client.get_notes(invitation='openreview.net/Support/-/Request_Form')[0]

        now = datetime.datetime.now()
        start_date = now - datetime.timedelta(days=2)
        due_date = now + datetime.timedelta(days=3)

        # review stage
        review_stage_note=pc_client.post_note(openreview.Note(
            content={
                'review_start_date': start_date.strftime('%Y/%m/%d'),
                'review_deadline': due_date.strftime('%Y/%m/%d'),
                'make_reviews_public': 'No, reviews should NOT be revealed publicly when they are posted',
                'release_reviews_to_authors': 'Yes, reviews should be revealed when they are posted to the paper\'s authors',
                'release_reviews_to_reviewers': 'Review should not be revealed to any reviewer, except to the author of the review',
                'email_program_chairs_about_reviews': 'No, do not email program chairs about received reviews',
            },
            forum=request_form.forum,
            invitation='openreview.net/Support/-/Request{}/Review_Stage'.format(request_form.number),
            readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
            replyto=request_form.forum,
            referent=request_form.forum,
            signatures=['~Program_ICAPSChair1'],
            writers=[]
        ))
        helpers.await_queue()

        helpers.await_queue_edit(openreview_client, 'PRL/2023/ICAPS/-/Official_Review-0-1', count=2)

        submissions = openreview_client.get_notes(invitation='PRL/2023/ICAPS/-/Submission', sort='number:asc')

        for submission in submissions:
            reviews = openreview_client.get_notes(invitation=f'PRL/2023/ICAPS/Submission{submission.number}/-/Official_Review') 
            assert len(reviews) == 1
            assert f'PRL/2023/ICAPS/Submission{submission.number}/Authors' in reviews[0].readers


    def test_enable_camera_ready_revisions(self, client, openreview_client, helpers, selenium, request_page):

        publication_chair_client = openreview.Client(username='publicationchair@mail.com', password=helpers.strong_password)
        request_form=publication_chair_client.get_notes(invitation='openreview.net/Support/-/Request_Form')[0]

        now = datetime.datetime.now()
        due_date = now + datetime.timedelta(days=3)

        # post submission revision stage note
        revision_stage_note = publication_chair_client.post_note(openreview.Note(
            content={
                'submission_revision_name': 'Camera_Ready_Revision',
                'submission_revision_deadline': due_date.strftime('%Y/%m/%d'),
                'accepted_submissions_only': 'Enable revision for accepted submissions only',
                'submission_author_edition': 'Do not allow any changes to author lists',
                'submission_revision_additional_options': {
                    "supplementary_materials": {
                        "value": {
                            "param": {
                                "type": "file",
                                "extensions": [
                                    "zip",
                                    "pdf",
                                    "tgz",
                                    "gz"
                                ],
                                "maxSize": 100
                            }
                        },
                        "description": "All supplementary material must be self-contained and zipped into a single file. Note that supplementary material will be visible to reviewers and the public throughout and after the review period, and ensure all material is anonymized. The maximum file size is 100MB.",
                        "order": 1
                    },
                },
                'submission_revision_remove_options': ['title', 'pdf', 'keywords', 'authors', 'authorids']
            },
            forum=request_form.forum,
            invitation='openreview.net/Support/-/Request{}/Submission_Revision_Stage'.format(request_form.number),
            readers=['{}/Program_Chairs'.format('PRL/2023/ICAPS'), 'openreview.net/Support', '{}/Publication_Chairs'.format('PRL/2023/ICAPS')],
            referent=request_form.forum,
            replyto=request_form.forum,
            signatures=['~Publication_ICAPSChair1'],
            writers=[]
        ))
        assert revision_stage_note
        helpers.await_queue()

        helpers.await_queue_edit(openreview_client, 'PRL/2023/ICAPS/-/Camera_Ready_Revision-0-1', count=1)

        process_logs = client.get_process_logs(id = revision_stage_note.id)
        assert len(process_logs) == 1
        assert process_logs[0]['status'] == 'ok'

        invitations = openreview_client.get_invitations(invitation='PRL/2023/ICAPS/-/Camera_Ready_Revision')
        assert len(invitations) == 7
        invitation = openreview_client.get_invitation(id='PRL/2023/ICAPS/Submission1/-/Camera_Ready_Revision')
        assert 'authors' not in invitation.edit['note']['content']
        assert 'authorids' not in invitation.edit['note']['content']

        request_page(selenium, 'http://localhost:3030/group?id=PRL/2023/ICAPS/Publication_Chairs', publication_chair_client.token, wait_for_element='header')
        notes_panel = selenium.find_element(By.ID, 'notes')
        assert notes_panel
        tabs = notes_panel.find_element(By.CLASS_NAME, 'tabs-container')
        assert tabs
        assert tabs.find_element(By.LINK_TEXT, "Accepted Submissions")

    def test_enable_opt_in_rejected_submissions(self, client, openreview_client, helpers, selenium, request_page):

        ## let authors decide if they want ther rejected submissions to be public
        pc_client=openreview.Client(username='pc@icaps.cc', password=helpers.strong_password)
        pc_client_v2=openreview.api.OpenReviewClient(username='pc@icaps.cc', password=helpers.strong_password)
        request_form=pc_client.get_notes(invitation='openreview.net/Support/-/Request_Form')[0]

        venue = openreview.helpers.get_conference(client, request_form.id, support_user='openreview.net/Support')

        now = datetime.datetime.now()
        due_date = now + datetime.timedelta(days=3)
        venue.custom_stage = openreview.stages.CustomStage(name='Opt_In_Public_Release',
            reply_to=openreview.stages.CustomStage.ReplyTo.FORUM,
            source={ 'venueid': ['PRL/2023/ICAPS', 'PRL/2023/ICAPS/Submission', 'PRL/2023/ICAPS/Rejected_Submission'], 'with_decision_accept': False },
            due_date=due_date,
            exp_date=due_date + datetime.timedelta(days=1),
            invitees=[openreview.stages.CustomStage.Participants.AUTHORS],
            readers=[openreview.stages.CustomStage.Participants.PROGRAM_CHAIRS, openreview.stages.CustomStage.Participants.SIGNATURES],
            content={
                'opt_in_public_release': {
                    'order': 1,
                    'description': 'Check the option to agree to release your submisison to the public.',
                    'value': {
                        'param': {
                            'type': 'string',
                            'input': 'checkbox',
                            'enum': ['I and my co-authors agree to release our submission to the public.']
                        }
                    }
                }
            },
            notify_readers=True,
            email_sacs=False)

        venue.create_custom_stage()

        helpers.await_queue_edit(openreview_client, 'PRL/2023/ICAPS/-/Opt_In_Public_Release-0-1', count=1)

        invitations = openreview_client.get_invitations(invitation='PRL/2023/ICAPS/-/Opt_In_Public_Release')
        assert len(invitations) == 3

        ids = [invitation.id for invitation in invitations]
        assert 'PRL/2023/ICAPS/Submission3/-/Opt_In_Public_Release' in ids
        assert 'PRL/2023/ICAPS/Submission6/-/Opt_In_Public_Release' in ids
        assert 'PRL/2023/ICAPS/Submission9/-/Opt_In_Public_Release' in ids

    
    def test_post_decision_for_new_submission(self, client, openreview_client, helpers):

        pc_client=openreview.Client(username='pc@icaps.cc', password=helpers.strong_password)
        pc_client_v2=openreview.api.OpenReviewClient(username='pc@icaps.cc', password=helpers.strong_password)
        request_form=pc_client.get_notes(invitation='openreview.net/Support/-/Request_Form')[0]

        submissions = openreview_client.get_notes(invitation='PRL/2023/ICAPS/-/Submission', sort='number:asc')
        assert len(submissions) == 12

        accept_decision = pc_client_v2.post_note_edit(
            invitation=f'PRL/2023/ICAPS/Submission{submissions[10].number}/-/Decision',
                signatures=['PRL/2023/ICAPS/Program_Chairs'],
                note=openreview.api.Note(
                    content={
                        'decision': { 'value': 'Accept' },
                        'comment': { 'value': 'Comment by PCs.' }
                    }
                )
            )
        
        helpers.await_queue_edit(openreview_client, edit_id=accept_decision['id'])

        assert f'PRL/2023/ICAPS/Submission11/Authors' in openreview_client.get_group('PRL/2023/ICAPS/Authors/Accepted').members

        reject_decision = pc_client_v2.post_note_edit(
            invitation=f'PRL/2023/ICAPS/Submission{submissions[11].number}/-/Decision',
                signatures=['PRL/2023/ICAPS/Program_Chairs'],
                note=openreview.api.Note(
                    content={
                        'decision': { 'value': 'Reject' },
                        'comment': { 'value': 'Comment by PCs.' }
                    }
                )
            )
        
        helpers.await_queue_edit(openreview_client, edit_id=reject_decision['id'])        

        assert f'PRL/2023/ICAPS/Submission12/Authors' not in openreview_client.get_group('PRL/2023/ICAPS/Authors/Accepted').members

        invitation = client.get_invitation(f'openreview.net/Support/-/Request{request_form.number}/Post_Decision_Stage')
        invitation.cdate = openreview.tools.datetime_millis(datetime.datetime.now())
        client.post_invitation(invitation)

        short_name = 'PRL ICAPS 2023'
        post_decision_stage_note = pc_client.post_note(openreview.Note(
            content={
                'reveal_authors': 'No, I don\'t want to reveal any author identities.',
                'submission_readers': 'All program committee (all reviewers, all area chairs, all senior area chairs if applicable)',
                'home_page_tab_names': {
                    'Accept': 'Accept',
                    'Invite to Venue': 'Invite to Venue',
                    'Reject': 'Submitted'
                },
                'send_decision_notifications': 'Yes, send an email notification to the authors',
                'accept_email_content': f'''Dear {{{{fullname}}}},

Thank you for submitting your paper, {{{{submission_title}}}}, to {short_name}. We are delighted to inform you that your submission has been accepted. Congratulations!
You can find the final reviews for your paper on the submission page in OpenReview at: {{{{forum_url}}}}

Best,
{short_name} Program Chairs
''',
                'invite_to_venue_email_content': f'''Dear {{{{fullname}}}},

Thank you for submitting your paper, {{{{submission_title}}}}, to {short_name}. We are delighted to inform you that your submission has been invited to the venue. Congratulations!
You can find the final reviews for your paper on the submission page in OpenReview at: {{{{forum_url}}}}

Best,
{short_name} Program Chairs
''',
                'reject_email_content': f'''Dear {{{{fullname}}}},

Thank you for submitting your paper, {{{{submission_title}}}}, to {short_name}. We regret to inform you that your submission was not accepted.
You can find the final reviews for your paper on the submission page in OpenReview at: {{{{forum_url}}}}

Best,
{short_name} Program Chairs
'''
            },
            forum=request_form.forum,
            invitation=invitation.id,
            readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
            replyto=request_form.forum,
            referent=request_form.forum,
            signatures=['~Program_ICAPSChair1'],
            writers=[]
        ))
        assert post_decision_stage_note
        helpers.await_queue()

        submissions = openreview_client.get_notes(invitation='PRL/2023/ICAPS/-/Submission', sort='number:asc')
        assert len(submissions) == 12

        assert submissions[10].readers == [
            'PRL/2023/ICAPS',
            'PRL/2023/ICAPS/Reviewers',
            'PRL/2023/ICAPS/Publication_Chairs',
            f'PRL/2023/ICAPS/Submission{submissions[10].number}/Authors'
        ]
        assert submissions[10].content['authors']['readers'] == [
            'PRL/2023/ICAPS',
            f'PRL/2023/ICAPS/Submission{submissions[10].number}/Authors',
            'PRL/2023/ICAPS/Publication_Chairs'
        ]
        assert submissions[10].content['venueid']['value'] == 'PRL/2023/ICAPS'
        assert submissions[10].content['venue']['value'] == 'PRL ICAPS 2023'

        assert submissions[11].readers == [
            'PRL/2023/ICAPS',
            'PRL/2023/ICAPS/Reviewers',
            f'PRL/2023/ICAPS/Submission{submissions[11].number}/Authors'
        ]
        assert submissions[11].content['authors']['readers'] == [
            'PRL/2023/ICAPS',
            f'PRL/2023/ICAPS/Submission{submissions[11].number}/Authors'
        ]
        assert submissions[11].content['venueid']['value'] == 'PRL/2023/ICAPS/Rejected_Submission'
        assert submissions[11].content['venue']['value'] == 'Submitted to PRL ICAPS 2023'

        messages = openreview_client.get_messages(subject=f'[PRL ICAPS 2023] Decision notification for your submission 1:.*')
        assert len(messages) == 3
        assert 'We are delighted to inform you that your submission has been accepted.' in messages[0]['content']['text']

        messages = openreview_client.get_messages(subject=f'[PRL ICAPS 2023] Decision notification for your submission 11:.*')
        assert len(messages) == 3 

        messages = openreview_client.get_messages(subject=f'[PRL ICAPS 2023] Decision notification for your submission 12:.*')
        assert len(messages) == 3


        invitations = openreview_client.get_invitations(invitation='PRL/2023/ICAPS/-/Opt_In_Public_Release')
        assert len(invitations) == 4

        ids = [invitation.id for invitation in invitations]
        assert 'PRL/2023/ICAPS/Submission3/-/Opt_In_Public_Release' in ids
        assert 'PRL/2023/ICAPS/Submission6/-/Opt_In_Public_Release' in ids
        assert 'PRL/2023/ICAPS/Submission9/-/Opt_In_Public_Release' in ids
        assert 'PRL/2023/ICAPS/Submission12/-/Opt_In_Public_Release' in ids


        invitations = openreview_client.get_invitations(invitation='PRL/2023/ICAPS/-/Camera_Ready_Revision')
        assert len(invitations) == 8
        invitation = openreview_client.get_invitation(id='PRL/2023/ICAPS/Submission11/-/Camera_Ready_Revision')
        assert 'authors' not in invitation.edit['note']['content']
        assert 'authorids' not in invitation.edit['note']['content']

        edit = pc_client_v2.get_note_edit(accept_decision['id'])
        assert edit.note.content['decision']['value'] == 'Accept'

        deleted_decision = pc_client_v2.post_note_edit(
            invitation=f'PRL/2023/ICAPS/Submission11/-/Decision',
                signatures=['PRL/2023/ICAPS/Program_Chairs'],
                note=openreview.api.Note(
                    id=accept_decision['note']['id'],
                    ddate=openreview.tools.datetime_millis(datetime.datetime.now()),
                    content={
                        'decision': { 'value': 'Accept' },
                        'comment': { 'value': 'Comment by PCs.' }
                    }
                )
            )
        
        helpers.await_queue_edit(openreview_client, edit_id=deleted_decision['id'])

        assert f'PRL/2023/ICAPS/Submission11/Authors' not in openreview_client.get_group('PRL/2023/ICAPS/Authors/Accepted').members

        messages = openreview_client.get_messages(subject=f'[PRL ICAPS 2023] Decision deleted on your submission - Paper Number: 11, Paper Title: "Paper title 11"')
        assert len(messages) == 3

        invitations = openreview_client.get_invitations(invitation='PRL/2023/ICAPS/-/Camera_Ready_Revision')
        assert len(invitations) == 7

        invitation = openreview_client.get_invitation(id='PRL/2023/ICAPS/Submission11/-/Camera_Ready_Revision')
        assert invitation.ddate is not None

        updated_decision = pc_client_v2.post_note_edit(
            invitation=f'PRL/2023/ICAPS/Submission12/-/Decision',
                signatures=['PRL/2023/ICAPS/Program_Chairs'],
                note=openreview.api.Note(
                    id=reject_decision['note']['id'],
                    content={
                        'decision': { 'value': 'Accept' },
                        'comment': { 'value': 'Comment by PCs.' }
                    }
                )
            )

        helpers.await_queue_edit(openreview_client, edit_id=updated_decision['id'])

        assert f'PRL/2023/ICAPS/Submission12/Authors' in openreview_client.get_group('PRL/2023/ICAPS/Authors/Accepted').members

        invitations = openreview_client.get_invitations(invitation='PRL/2023/ICAPS/-/Camera_Ready_Revision')
        assert len(invitations) == 8

        invitations = openreview_client.get_invitations(invitation='PRL/2023/ICAPS/-/Opt_In_Public_Release')
        assert len(invitations) == 3

        ids = [invitation.id for invitation in invitations]
        assert 'PRL/2023/ICAPS/Submission3/-/Opt_In_Public_Release' in ids
        assert 'PRL/2023/ICAPS/Submission6/-/Opt_In_Public_Release' in ids
        assert 'PRL/2023/ICAPS/Submission9/-/Opt_In_Public_Release' in ids
        assert 'PRL/2023/ICAPS/Submission12/-/Opt_In_Public_Release' not in ids

        invitation = client.get_invitation(f'openreview.net/Support/-/Request{request_form.number}/Post_Decision_Stage')
        invitation.cdate = openreview.tools.datetime_millis(datetime.datetime.now())
        client.post_invitation(invitation)

        short_name = 'PRL ICAPS 2023'
        post_decision_stage_note = pc_client.post_note(openreview.Note(
            content={
                'reveal_authors': 'No, I don\'t want to reveal any author identities.',
                'submission_readers': 'All program committee (all reviewers, all area chairs, all senior area chairs if applicable)',
                'home_page_tab_names': {
                    'Accept': 'Accept',
                    'Invite to Venue': 'Invite to Venue',
                    'Reject': 'Submitted'
                },
                'send_decision_notifications': 'Yes, send an email notification to the authors',
                'accept_email_content': f'''Dear {{{{fullname}}}},

Thank you for submitting your paper, {{{{submission_title}}}}, to {short_name}. We are delighted to inform you that your submission has been accepted. Congratulations!
You can find the final reviews for your paper on the submission page in OpenReview at: {{{{forum_url}}}}

Best,
{short_name} Program Chairs
''',
                'invite_to_venue_email_content': f'''Dear {{{{fullname}}}},

Thank you for submitting your paper, {{{{submission_title}}}}, to {short_name}. We are delighted to inform you that your submission has been invited to the venue. Congratulations!
You can find the final reviews for your paper on the submission page in OpenReview at: {{{{forum_url}}}}

Best,
{short_name} Program Chairs
''',
                'reject_email_content': f'''Dear {{{{fullname}}}},

Thank you for submitting your paper, {{{{submission_title}}}}, to {short_name}. We regret to inform you that your submission was not accepted.
You can find the final reviews for your paper on the submission page in OpenReview at: {{{{forum_url}}}}

Best,
{short_name} Program Chairs
'''
            },
            forum=request_form.forum,
            invitation=invitation.id,
            readers=['PRL/2023/ICAPS/Program_Chairs', 'openreview.net/Support'],
            replyto=request_form.forum,
            referent=request_form.forum,
            signatures=['~Program_ICAPSChair1'],
            writers=[]
        ))
        assert post_decision_stage_note
        helpers.await_queue()

        submissions = openreview_client.get_notes(invitation='PRL/2023/ICAPS/-/Submission', sort='number:asc')
        assert len(submissions) == 12

        ## TODO: rollback venueid
        assert submissions[10].readers == [
            'PRL/2023/ICAPS',
            'PRL/2023/ICAPS/Reviewers',
            'PRL/2023/ICAPS/Publication_Chairs',
            f'PRL/2023/ICAPS/Submission{submissions[10].number}/Authors'
        ]
        assert submissions[10].content['authors']['readers'] == [
            'PRL/2023/ICAPS',
            f'PRL/2023/ICAPS/Submission{submissions[10].number}/Authors',
            'PRL/2023/ICAPS/Publication_Chairs'
        ]
        assert submissions[10].content['venueid']['value'] == 'PRL/2023/ICAPS'
        assert submissions[10].content['venue']['value'] == 'PRL ICAPS 2023' 

        assert submissions[11].readers == [
            'PRL/2023/ICAPS',
            'PRL/2023/ICAPS/Reviewers',
            'PRL/2023/ICAPS/Publication_Chairs',
            f'PRL/2023/ICAPS/Submission{submissions[11].number}/Authors'
        ]
        assert submissions[11].content['authors']['readers'] == [
            'PRL/2023/ICAPS',
            f'PRL/2023/ICAPS/Submission{submissions[11].number}/Authors',
            'PRL/2023/ICAPS/Publication_Chairs'
        ]
        assert submissions[11].content['venueid']['value'] == 'PRL/2023/ICAPS'
        assert submissions[11].content['venue']['value'] == 'PRL ICAPS 2023'

    def test_preferred_emails_authors(self, client, openreview_client, helpers, selenium, request_page):

        pc_client_v2=openreview.api.OpenReviewClient(username='pc@icaps.cc', password=helpers.strong_password)

        openreview_client.post_invitation_edit(
            invitations='PRL/2023/ICAPS/-/Edit',
            signatures=['~Super_User1'],
            invitation=openreview.api.Invitation(
                id='PRL/2023/ICAPS/-/Preferred_Emails',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now()) + 2000,
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id='PRL/2023/ICAPS/-/Preferred_Emails-0-0', count=2)        

        notes = pc_client_v2.get_all_notes(content={ 'venueid': 'PRL/2023/ICAPS' })

        all_accepted_authors = set()
        for note in notes:
            for author in note.content['authorids']['value']:
                all_accepted_authors.add(author)

        assert len(all_accepted_authors) == 9

        profiles =openreview.tools.get_profiles(pc_client_v2, list(all_accepted_authors), with_preferred_emails='PRL/2023/ICAPS/-/Preferred_Emails')
        assert len(profiles) == 9

        test_profile = [p for p in profiles if p.id == '~SomeFirstName_User1']
        test_profile[0].content['preferredEmail'] == 'test@mail.com'
        test_profile[0].get_preferred_email() == 'test@mail.com'
