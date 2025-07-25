import openreview
import pytest
import time
import json
import datetime
import random
import os
import re
from string import ascii_lowercase as alc
from openreview.api import OpenReviewClient
from openreview.api import Note
from openreview.journal import Journal
from openreview.journal import JournalRequest
from selenium.webdriver.common.by import By

class TestJournal():

    @pytest.fixture(scope="class")
    def journal(self, openreview_client, helpers):

        venue_id = 'TMLR'
        fabian_client=OpenReviewClient(username='fabian@mail.com', password=helpers.strong_password)
        fabian_client.impersonate('TMLR/Editors_In_Chief')

        requests = openreview_client.get_notes(invitation='openreview.net/Support/-/Journal_Request', content={ 'venue_id': venue_id })

        return JournalRequest.get_journal(fabian_client, requests[0].id)

    def test_setup(self, openreview_client, request_page, selenium, helpers, journal_request):

        venue_id = 'TMLR'

        ## Support Role
        helpers.create_user('fabian@mail.com', 'Fabian', 'Pedregosa')

        ## Editors in Chief
        helpers.create_user('raia@mail.com', 'Raia', 'Hadsell')
        helpers.create_user('kyunghyun@mail.com', 'Kyunghyun', 'Cho')

        ## Action Editors
        helpers.create_user('joelle@mailseven.com', 'Joelle', 'Pineau')
        helpers.create_user('yan@mail.com', 'Ryan', 'Adams')
        helpers.create_user('samy@bengio.com', 'Samy', 'Bengio')
        helpers.create_user('yoshua@mail.com', 'Yoshua', 'Bengio')
        helpers.create_user('corinna@mail.com', 'Corinna', 'Cortes')
        helpers.create_user('ivan@mail.com', 'Ivan', 'Titov')
        helpers.create_user('shakir@mail.com', 'Shakir', 'Mohamed')
        helpers.create_user('silvia@apple.com', 'Silvia', 'Villa')

        ## Reviewers
        helpers.create_user('david@mailone.com', 'David', 'Belanger')
        helpers.create_user('javier@mailtwo.com', 'Javier', 'Burroni')
        helpers.create_user('carlos@mailthree.com', 'Carlos', 'Mondragon')
        helpers.create_user('andrewmc@mailfour.com', 'Andrew', 'McCallumm')
        helpers.create_user('hugo@mailsix.com', 'Hugo', 'Larochelle')
        helpers.create_user('david_2@mailone.com', 'David K', 'Belanger')
        openreview_client.merge_profiles('~David_Belanger1', '~David_K_Belanger1')

        ## External Reviewers
        helpers.create_user('melisa@mailten.com', 'Melisa', 'Bok')

        ## Authors
        helpers.create_user('melissa@maileight.com', 'Melissa', 'Eight')
        helpers.create_user('celeste@mailnine.com', 'Celeste Ana', 'Martinez')

        #post journal request form
        request_form = openreview_client.post_note_edit(invitation= 'openreview.net/Support/-/Journal_Request',
            signatures = ['openreview.net/Support'],
            note = Note(
                signatures = ['openreview.net/Support'],
                content = {
                    'official_venue_name': {'value': 'Transactions on Machine Learning Research'},
                    'abbreviated_venue_name' : {'value': 'TMLR'},
                    'venue_id': {'value': 'TMLR'},
                    'contact_info': {'value': 'tmlr@jmlr.org'},
                    'secret_key': {'value': '1234'},
                    'support_role': {'value': '~Fabian_Pedregosa1' },
                    'editors': {'value': ['~Raia_Hadsell1', '~Kyunghyun_Cho1'] },
                    'website': {'value': 'jmlr.org/tmlr' },
                    'settings': {
                        'value': {
                            'submission_public': True,
                            'assignment_delay': 5,
                            'submission_name': 'Submission',
                            'submission_license': 'CC BY-SA 4.0',
                            'eic_submission_notification': False,
                            'certifications': [
                                'Featured Certification',
                                'Reproducibility Certification',
                                'Survey Certification'
                            ],
                            'eic_certifications': [
                                'Outstanding Certification'
                            ],
                            'event_certifications': [
                                'lifelong-ml.cc/CoLLAs/2023/Journal_Track'
                            ],                            
                            'submission_length': [
                                'Regular submission (no more than 12 pages of main content)', 
                                'Long submission (more than 12 pages of main content)'
                            ],
                            'issn': '2835-8856',
                            'website_urls': {
                                'editorial_board': 'https://jmlr.org/tmlr/editorial-board.html',
                                'evaluation_criteria': 'https://jmlr.org/tmlr/editorial-policies.html#evaluation',
                                'reviewer_guide': 'https://jmlr.org/tmlr/reviewer-guide.html',
                                'editorial_policies': 'https://jmlr.org/tmlr/editorial-policies.html',
                                'faq': 'https://jmlr.org/tmlr/contact.html',
                                'videos': 'https://tmlr.infinite-conf.org',
                                'certifications_criteria': 'https://jmlr.org/tmlr/editorial-policies.html#certifications'
                            },
                            'editors_email': 'tmlr-editors@jmlr.org',
                            'skip_ac_recommendation': False,
                            'number_of_reviewers': 3,
                            'reviewers_max_papers': 6,
                            'ae_recommendation_period': 1,
                            'under_review_approval_period': 1,
                            'reviewer_assignment_period': 1,
                            'review_period': 2,
                            'discussion_period' : 2,
                            'recommendation_period': 2,
                            'decision_period': 1,
                            'camera_ready_period': 4,
                            'camera_ready_verification_period': 1,
                            'archived_action_editors': True,
                            'archived_reviewers': True,
                            'expert_reviewers': True,
                            'external_reviewers': True,
                            'expertise_model': 'specter+mfr',
                            'review_additional_fields': {
                                'strengths_and_weaknesses': False,
                                'summary_of_contributions': {
                                    'order': 1,
                                    'description': 'Please summarize the contributions of the paper in your own words. Please also list any key strengths and/or weaknesses, but please be mindful that this is NOT a substitute for the next two text boxes. Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq.',
                                    'value': {
                                        'param': {
                                            'maxLength': 200000,
                                            'input': 'textarea',
                                            'type': 'string',
                                            'markdown': True
                                        }
                                    }
                                },
                                'claims_and_evidence': {
                                    'order': 2,
                                    'description': 'Learn more about TMLR\'s evaluation criteria at https://jmlr.org/tmlr/editorial-policies.html#evaluation.',
                                    'value': {
                                        'param': {
                                            'fieldName': f'Are the claims made in the submission supported by accurate, convincing and clear evidence?',
                                            'type': 'string',
                                            'enum': ['Yes', 'No'],
                                            'input': 'radio'
                                        }
                                    }
                                },
                                'claims_explanation': {
                                    'order': 3,
                                    'description': 'Learn more about TMLR\'s evaluation criteria at https://jmlr.org/tmlr/editorial-policies.html#evaluation.',
                                    'value': {
                                        'param': {
                                            'fieldName': 'Explain your answer above',
                                            'type': 'string',
                                            'maxLength': 200000,
                                            'input': 'textarea',
                                            'markdown': True
                                        }
                                    }
                                },
                                'audience': {
                                    'order': 4,
                                    'description': 'Learn more about TMLR\'s evaluation criteria at https://jmlr.org/tmlr/editorial-policies.html#evaluation.',
                                    'value': {
                                        'param': {
                                            'fieldName': 'Would at least some individuals in TMLR\'s audience be interested in knowing the findings of this paper?',
                                            'type': 'string',
                                            'enum': ['Yes', 'No'],
                                            'input': 'radio'
                                        }
                                    }
                                },
                                'audience_explanation': {
                                    'order': 5,
                                    'description': 'Learn more about TMLR\'s evaluation criteria at https://jmlr.org/tmlr/editorial-policies.html#evaluation.',
                                    'value': {
                                        'param': {
                                            'fieldName': 'Explain your answer above',
                                            'type': 'string',
                                            'maxLength': 200000,
                                            'input': 'textarea',
                                            'markdown': True
                                        }
                                    }
                                },
                                'requested_changes': {
                                    'order': 6,
                                    'description': 'List of proposed adjustments to the submission, specifying for each whether they are critical to securing your recommendation for acceptance or would simply strengthen the work in your view (max 200000 characters). Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq.',
                                    'value': {
                                        'param': {
                                            'maxLength': 200000,
                                            'input': 'textarea',
                                            'type': 'string',
                                            'markdown': True
                                        }
                                    }
                                },
                                'broader_impact_concerns': {
                                    'order': 7,
                                    'description': 'Brief description of any concerns on the ethical implications of the work that would require adding a Broader Impact Statement (if one is not present) or that are not sufficiently addressed in the Broader Impact Statement section (if one is present) (max 200000 characters). Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq.',
                                    'value': {
                                        'param': {
                                            'maxLength': 200000,
                                            'input': 'textarea',
                                            'type': 'string',
                                            'markdown': True
                                        }
                                    }
                                },
                                'additional_comments': {
                                    'order': 10,
                                    'value': {
                                        'param': {
                                            'type': 'string',
                                            'maxLength': 200000,
                                            'input': 'textarea',
                                            'markdown': True,
                                            'optional': True
                                        }
                                    }
                                }
                            },
                            'official_recommendation_additional_fields': {
                                'pilot_recommendation_to_iclr_track': False,
                                'pilot_explain_recommendation_to_iclr_track': False,
                                'recommendation_to_iclr_track': {
                                    'order': 98,
                                    'description': 'Would you recommend this work be invited for presentation at the ICLR Journal-to-Conference Track? Recall that TMLR\'s acceptance criteria are that a work must be sound and of interest to the TMLR audience. Above these requirements, a paper in the ICLR Journal-to-Conference Track should also stand out in novelty or predicted significance for the field (i.e., comparable to the level of a paper in ICLR\'s regular conference track). **Your anonymized response will be shared with ICLR**',
                                    'value': {
                                        'param': {
                                            'fieldName': 'Recommendation to ICLR Journal-to-Conference Track',
                                            'type': 'string',
                                            'enum': ['Strongly Recommend', 'Weakly Recommend', 'Weakly Oppose', 'Strongly Oppose'],
                                            'input': 'radio',
                                        }
                                    },
                                    'readers': ['TMLR', 'TMLR/Paper${7/content/noteNumber/value}/Action_Editors', '${5/signatures}']
                                },
                                'explain_recommendation_to_iclr_track': {
                                    'order': 98,
                                    'description': '**Your anonymized response will be shared with ICLR**',
                                    'value': {
                                        'param': {
                                            'fieldName': 'Explain your recommendation to the ICLR Journal-to-Conference Track',
                                            'type': 'string',
                                            'maxLength': 50000,
                                            'markdown': True,
                                            'input': 'textarea'
                                        }
                                    },
                                    'readers': ['TMLR', 'TMLR/Paper${7/content/noteNumber/value}/Action_Editors', '${5/signatures}']
                                }                                
                            },
                            'decision_additional_fields': {
                                'claims_and_evidence': {
                                    'order': 2,
                                    'description': 'Learn more about TMLR\'s evaluation criteria at https://jmlr.org/tmlr/editorial-policies.html#evaluation.',
                                    'value': {
                                        'param': {
                                            'fieldName': f'Are the claims made in the submission supported by accurate, convincing and clear evidence?',
                                            'type': 'string',
                                            'enum': ['Yes', 'No'],
                                            'input': 'radio'
                                        }
                                    }
                                },
                                'claims_explanation': {
                                    'order': 3,
                                    'description': 'Learn more about TMLR\'s evaluation criteria at https://jmlr.org/tmlr/editorial-policies.html#evaluation.',
                                    'value': {
                                        'param': {
                                            'fieldName': 'Explain your answer above',
                                            'type': 'string',
                                            'maxLength': 200000,
                                            'input': 'textarea',
                                            'markdown': True
                                        }
                                    }
                                },
                                'audience': {
                                    'order': 4,
                                    'description': 'Learn more about TMLR\'s evaluation criteria at https://jmlr.org/tmlr/editorial-policies.html#evaluation.',
                                    'value': {
                                        'param': {
                                            'fieldName': 'Would at least some individuals in TMLR\'s audience be interested in knowing the findings of this paper?',
                                            'type': 'string',
                                            'enum': ['Yes', 'No'],
                                            'input': 'radio'
                                        }
                                    }
                                },
                                'audience_explanation': {
                                    'order': 5,
                                    'description': 'Learn more about TMLR\'s evaluation criteria at https://jmlr.org/tmlr/editorial-policies.html#evaluation.',
                                    'value': {
                                        'param': {
                                            'fieldName': 'Explain your answer above',
                                            'type': 'string',
                                            'maxLength': 200000,
                                            'input': 'textarea',
                                            'markdown': True
                                        }
                                    }
                                },
                                'comment': False,
                                'additional_comments': {
                                    'order': 10,
                                    'description': 'If you request revisions, provide details on the expected changes. If you recommend a certification, explain the reasons for why the submission deserves this recognition.',
                                    'value': {
                                        'param': {
                                            'type': 'string',
                                            'maxLength': 200000,
                                            'input': 'textarea',
                                            'markdown': True,
                                            'optional': True
                                        }
                                    }
                                },
                                'pilot_recommendation_to_iclr_track': False,
                                'pilot_explain_recommendation_to_iclr_track': False,
                                'recommendation_to_iclr_track': {
                                    'order': 98,
                                    'description': 'Would you recommend this work be invited for presentation at the ICLR Journal-to-Conference Track? Recall that TMLR\'s acceptance criteria are that a work must be sound and of interest to the TMLR audience. Above these requirements, a paper in the ICLR Journal-to-Conference Track should also stand out in novelty or predicted significance for the field (i.e., comparable to the level of a paper in ICLR\'s regular conference track. **Your response will be shared with ICLR**',
                                    'value': {
                                        'param': {
                                            'fieldName': 'Recommendation to ICLR Journal-to-Conference Track',
                                            'type': 'string',
                                            'enum': ['Strongly Recommend', 'Weakly Recommend', 'Weakly Oppose', 'Strongly Oppose'],
                                            'input': 'radio',
                                        }
                                    },
                                    'readers': ['TMLR', 'TMLR/Paper${7/content/noteNumber/value}/Action_Editors']
                                },
                                'explain_recommendation_to_iclr_track': {
                                    'order': 98,
                                    'description': '**Your response will be shared with ICLR**',
                                    'value': {
                                        'param': {
                                            'fieldName': 'Explain your recommendation to the ICLR Journal-to-Conference Track',
                                            'type': 'string',
                                            'maxLength': 50000,
                                            'markdown': True,
                                            'input': 'textarea'
                                        }
                                    },
                                    'readers': ['TMLR', 'TMLR/Paper${7/content/noteNumber/value}/Action_Editors']
                                }                                
                            },
                            'assignment_delay_after_submitted_review': 0.0001   # ~ 1 minute
                        }
                    }
                }
            ))

        helpers.await_queue_edit(openreview_client, request_form['id'])

        openreview_client.add_members_to_group('TMLR/Expert_Reviewers', ['~Andrew_McCallumm1'])

        tmlr =  openreview_client.get_group('TMLR')
        assert tmlr
        assert tmlr.members == ['~Fabian_Pedregosa1', 'TMLR/Editors_In_Chief']
        assert tmlr.content['submission_id']['value'] == 'TMLR/-/Submission'
        assert tmlr.content['certifications']['value'] == ['Featured Certification', 'Reproducibility Certification', 'Survey Certification']
        assert tmlr.content['eic_certifications']['value'] == ['Outstanding Certification']
        assert tmlr.content['expert_reviewer_certification']['value'] == 'Expert Certification'
        assert tmlr.content['event_certifications']['value'] == ['lifelong-ml.cc/CoLLAs/2023/Journal_Track']

        invitation = openreview_client.get_invitation('TMLR/-/Accepted')
        assert invitation.edit['note']['content']['certifications']['value']['param']['enum'] == [
            "Featured Certification",
            "Reproducibility Certification",
            "Survey Certification",
            "Expert Certification"
        ]
        assert 'expert_reviewers' in invitation.edit['note']['content']
        assert openreview_client.get_group('TMLR/Reviewers/Archived')

        openreview_client.post_group_edit(
            invitation='TMLR/-/Edit',
            signatures=['TMLR'],
            group=openreview.api.Group(
                id='TMLR/Authors',
                content={
                    'new_submission_email_template_script': { 'delete': True },
                    'official_recommendation_starts_email_template_script': { 'delete': True }
                }
            )
        )

        assert openreview.tools.get_invitation(openreview_client, 'TMLR/-/Preferred_Emails')
        assert openreview_client.get_edges_count(invitation='TMLR/-/Preferred_Emails') == 0

    def test_invite_action_editors(self, journal, openreview_client, request_page, selenium, helpers):

        venue_id = 'TMLR'
        request_notes = openreview_client.get_notes(invitation='openreview.net/Support/-/Journal_Request', content= { 'venue_id': 'TMLR' })
        request_note_id = request_notes[0].id
        journal = JournalRequest.get_journal(openreview_client, request_note_id)

        recruitment_status = journal.invite_action_editors(message='Test {{fullname}},  {{accept_url}}, {{decline_url}}', subject='Invitation to be an Action Editor', invitees=['User@mail.com', 'joelle@mailseven.com', '~Ryan_Adams1', '~Samy_Bengio1', '~Yoshua_Bengio1', '~Corinna_Cortes1', '~Ivan_Titov1', '~Shakir_Mohamed1', '~Silvia_Villa1'])
        print(recruitment_status)
        assert len(recruitment_status['invited']) == 9
        assert recruitment_status['errors'] == {}
        invited_group = openreview_client.get_group('TMLR/Action_Editors/Invited')
        assert invited_group.members == ['user@mail.com', '~Joelle_Pineau1', '~Ryan_Adams1', '~Samy_Bengio1', '~Yoshua_Bengio1', '~Corinna_Cortes1', '~Ivan_Titov1', '~Shakir_Mohamed1', '~Silvia_Villa1']

        messages = openreview_client.get_messages(subject = 'Invitation to be an Action Editor')
        assert len(messages) == 9

        for message in messages:
            text = message['content']['text']
            accept_url = re.search('https://.*response=Yes', text).group(0).replace('https://openreview.net', 'http://localhost:3030')
            request_page(selenium, accept_url, alert=True)

            notes = selenium.find_element(By.ID, 'notes')
            assert notes
            messages = notes.find_elements(By.TAG_NAME, 'h3')
            assert messages
            assert 'Thank you for accepting this invitation from Transactions on Machine Learning Research' == messages[0].text


        helpers.await_queue_edit(openreview_client, invitation = 'TMLR/Action_Editors/-/Recruitment')

        group = openreview_client.get_group('TMLR/Action_Editors')
        assert len(group.members) == 9
        assert '~Joelle_Pineau1' in group.members

        joelle_client = OpenReviewClient(username='joelle@mailseven.com', password=helpers.strong_password)
        request_page(selenium, "http://localhost:3030/group?id=TMLR/Action_Editors", joelle_client.token, wait_for_element='group-container')
        header = selenium.find_element(By.ID, 'header')
        assert header
        titles = header.find_elements(By.TAG_NAME, 'strong')
        assert 'Reviewer Assignment Browser:' in titles[0].text
        assert 'Journal Recruitment:' in titles[1].text
        assert 'Reviewer Report:' in titles[2].text

    def test_invite_reviewers(self, journal, openreview_client, request_page, selenium, helpers):

        venue_id = 'TMLR'

        request_notes = openreview_client.get_notes(invitation='openreview.net/Support/-/Journal_Request', content= { 'venue_id': 'TMLR' })
        request_note_id = request_notes[0].id
        journal = JournalRequest.get_journal(openreview_client, request_note_id)

        journal.invite_reviewers(message='Test {{fullname}},  {{accept_url}}, {{decline_url}}', subject='Invitation to be an Reviewer', invitees=['zach@mail.com', '~David_Belanger1', '~Javier_Burroni1', '~Carlos_Mondragon1', '~Andrew_McCallumm1', '~Hugo_Larochelle1'])
        invited_group = openreview_client.get_group('TMLR/Reviewers/Invited')
        assert invited_group.members == ['zach@mail.com', '~David_Belanger1', '~Javier_Burroni1', '~Carlos_Mondragon1', '~Andrew_McCallumm1', '~Hugo_Larochelle1']

        messages = openreview_client.get_messages(subject = 'Invitation to be an Reviewer')
        assert len(messages) == 6

        for message in messages:
            text = message['content']['text']
            accept_url = re.search('https://.*response=Yes', text).group(0).replace('https://openreview.net', 'http://localhost:3030')
            request_page(selenium, accept_url, alert=True)

            notes = selenium.find_element(By.ID, 'notes')
            assert notes
            messages = notes.find_elements(By.TAG_NAME, 'h3')
            assert messages
            assert 'Thank you for accepting this invitation from Transactions on Machine Learning Research' == messages[0].text


        helpers.await_queue_edit(openreview_client, invitation = 'TMLR/Reviewers/-/Recruitment')

        group = openreview_client.get_group('TMLR/Reviewers')
        assert len(group.members) == 6
        assert '~Javier_Burroni1' in group.members

        status = journal.invite_reviewers(message='Test {name},  {accept_url}, {decline_url}', subject='Invitation to be an Reviewer', invitees=['javier@mailtwo.com'])
        messages = openreview_client.get_messages(to = 'javier@mailtwo.com', subject = 'Invitation to be an Reviewer')
        assert len(messages) == 1

        assert status.get('already_member')
        assert 'javier@mailtwo.com' in status.get('already_member')

    def test_submission(self, journal, openreview_client, test_client, helpers):

        ## Remove reviewers with no profile
        openreview_client.remove_members_from_group('TMLR/Action_Editors', 'user@mail.com')
        openreview_client.remove_members_from_group('TMLR/Reviewers', 'zach@mail.com')

        venue_id = journal.venue_id
        test_client = OpenReviewClient(username='test@mail.com', password=helpers.strong_password)
        raia_client = OpenReviewClient(username='raia@mail.com', password=helpers.strong_password)
        joelle_client = OpenReviewClient(username='joelle@mailseven.com', password=helpers.strong_password)


        ## Reviewers
        david_client=OpenReviewClient(username='david@mailone.com', password=helpers.strong_password)
        javier_client=OpenReviewClient(username='javier@mailtwo.com', password=helpers.strong_password)
        carlos_client=OpenReviewClient(username='carlos@mailthree.com', password=helpers.strong_password)
        andrew_client=OpenReviewClient(username='andrewmc@mailfour.com', password=helpers.strong_password)
        hugo_client=OpenReviewClient(username='hugo@mailsix.com', password=helpers.strong_password)

        ## Set a max quota
        david_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Custom_Max_Papers',
            readers=[venue_id, 'TMLR/Action_Editors', '~David_Belanger1', 'TMLR/Action_Editors/Archived'],
            writers=[venue_id, '~David_Belanger1'],
            signatures=['~David_Belanger1'],
            head='TMLR/Reviewers',
            tail='~David_Belanger1',
            weight=8
        ))

        peter_client=helpers.create_user('petersnow@yahoo.com', 'Peter', 'Snow')

        guest_client=OpenReviewClient()
        now = datetime.datetime.now()

        ## Post the submission 1
        submission_note_1 = test_client.post_note_edit(invitation='TMLR/-/Submission',
            signatures=['~SomeFirstName_User1'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title' },
                    'abstract': { 'value': 'Paper abstract' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight', 'Andrew McCallum']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1', '~Andrew_McCallumm1']},
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    #'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'submission_length': { 'value': 'Regular submission (no more than 12 pages of main content)'}
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_1['id'])
        note_id_1=submission_note_1['note']['id']
        assert submission_note_1['note']['license'] == 'CC BY-SA 4.0'

        messages = openreview_client.get_messages(to = 'test@mail.com', subject = '[TMLR] New submission to TMLR: Paper title')
        assert len(messages) == 0

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        edges = []
        for ae in openreview_client.get_group('TMLR/Action_Editors').members:
            edges.append(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Affinity_Score',
                readers=['TMLR', 'TMLR/Paper1/Authors', ae],
                writers=['TMLR'],
                signatures=['TMLR'],
                head=note_id_1,
                tail=ae,
                weight=0.5
            ))

        openreview_client.post_edges(edges)

        openreview_client.get_invitation('TMLR/Paper1/Action_Editors/-/Recommendation')

        messages = openreview_client.get_messages(to = 'test@mail.com', subject = '[TMLR] Suggest candidate Action Editor for your new TMLR submission')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == '''Hi SomeFirstName User,

Thank you for submitting your work titled "Paper title" to TMLR.

Before the review process starts, you need to submit three or more recommendations for an Action Editor that you believe has the expertise to oversee the evaluation of your work.

To do so, please follow this link: https://openreview.net/invitation?id=TMLR/Paper1/Action_Editors/-/Recommendation or check your tasks in the Author Console: https://openreview.net/group?id=TMLR/Authors

For more details and guidelines on the TMLR review process, visit jmlr.org/tmlr.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        author_group=openreview_client.get_group(f"{venue_id}/Paper1/Authors")
        assert author_group
        assert author_group.members == ['~SomeFirstName_User1', '~Melissa_Eight1', '~Andrew_McCallumm1']
        assert openreview_client.get_group(f"{venue_id}/Paper1/Reviewers")
        assert openreview_client.get_group(f"{venue_id}/Paper1/Action_Editors")

        note = openreview_client.get_note(note_id_1)
        assert note
        assert note.invitations == ['TMLR/-/Submission']
        assert note.readers == ['TMLR', 'TMLR/Paper1/Action_Editors', 'TMLR/Paper1/Authors']
        assert note.writers == ['TMLR', 'TMLR/Paper1/Authors']
        assert note.signatures == ['TMLR/Paper1/Authors']
        assert note.content['authorids']['value'] == ['~SomeFirstName_User1', '~Melissa_Eight1', '~Andrew_McCallumm1']
        assert note.content['venue']['value'] == 'Submitted to TMLR'
        assert note.content['venueid']['value'] == 'TMLR/Submitted'

        invitation = openreview_client.get_invitation(f"{venue_id}/Paper1/-/Official_Comment")
        assert invitation.edit['note']['readers']['param']['items'] == [
            { "value": "everyone", "optional": True },
            { "value": "TMLR/Editors_In_Chief", "optional": True },
            { "value": "TMLR/Paper1/Action_Editors", "optional": True },
            { "value": "TMLR/Paper1/Reviewers", "optional": True },
            { "inGroup": "TMLR/Paper1/Reviewers", "optional": True },
            { "value": "TMLR/Paper1/Authors", "optional": True }
        ]

        invitations = openreview_client.get_invitations(replyForum=note_id_1)
        assert len(invitations) == 10, ", ".join([i.id for i in invitations])
        assert f"{venue_id}/-/Submission" not in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Review_Approval" not in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Withdrawal"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Desk_Rejection"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Revision" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/-/Under_Review"  in [i.id for i in invitations]
        assert f"{venue_id}/-/Desk_Rejected" in [i.id for i in invitations]
        assert f"{venue_id}/-/Rejected" in [i.id for i in invitations]
        assert f"{venue_id}/-/Withdrawn" in [i.id for i in invitations]
        assert f"{venue_id}/-/Retracted" in [i.id for i in invitations]
        assert f"{venue_id}/-/Authors_Release" in [i.id for i in invitations]


        ## Check author reminders
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/Action_Editors/-/Recommendation',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 10)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 1)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/Action_Editors/-/Recommendation-0-0')

        messages = journal.client.get_messages(subject = '[TMLR] You are late in performing a task for your paper 1: Paper title')
        assert len(messages) == 3
        messages = journal.client.get_messages(to = 'test@mail.com', subject = '[TMLR] You are late in performing a task for your paper 1: Paper title')
        assert messages[0]['content']['text'] == f'''Hi SomeFirstName User,

Our records show that you are late on the current task:

  Task: Recommendation
  Submission: Paper title
  Number of days late: 1
  Link: https://openreview.net/group?id=TMLR/Authors#author-tasks

Please follow the provided link and complete your task ASAP.

We thank you for your cooperation.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        ## Post AE recommendations
        test_client.post_edge(openreview.api.Edge(
            invitation='TMLR/Action_Editors/-/Recommendation',
            head=note_id_1,
            tail='~Joelle_Pineau1',
            weight=1
        ))
        
        test_client.post_edge(openreview.api.Edge(
            invitation='TMLR/Action_Editors/-/Recommendation',
            head=note_id_1,
            tail='~Samy_Bengio1',
            weight=1
        ))

        test_client.post_edge(openreview.api.Edge(
            invitation='TMLR/Action_Editors/-/Recommendation',
            head=note_id_1,
            tail='~Yoshua_Bengio1',
            weight=1
        ))

        ## Check author reminders
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/Action_Editors/-/Recommendation',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 10)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 7)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/Action_Editors/-/Recommendation-0-1')

        messages = journal.client.get_messages(subject = '[TMLR] You are late in performing a task for your paper 1: Paper title')
        assert len(messages) == 3


        ## Update submission 1
        updated_submission_note_1 = test_client.post_note_edit(invitation='TMLR/Paper1/-/Revision',
            signatures=['TMLR/Paper1/Authors'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title UPDATED' },
                    'supplementary_material': { 'value': '/attachment/' + 'z' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'pdf': { 'value': '/pdf/22234qweoiuweroi22234qweoiuweroi12345678.pdf' },
                    'submission_length': { 'value': 'Regular submission (no more than 12 pages of main content)'}
                }
            ))
        helpers.await_queue_edit(openreview_client, edit_id=updated_submission_note_1['id'])

        messages = openreview_client.get_messages(subject='[TMLR] Revision posted on submission 1: Paper title UPDATED')
        assert len(messages) == 3

        note = openreview_client.get_note(note_id_1)
        assert note
        assert note.number == 1
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/Paper1/-/Revision']
        assert note.readers == ['TMLR', 'TMLR/Paper1/Action_Editors', 'TMLR/Paper1/Authors']
        assert note.writers == ['TMLR', 'TMLR/Paper1/Authors']
        assert note.signatures == ['TMLR/Paper1/Authors']
        assert note.content['title']['value'] == 'Paper title UPDATED'
        assert note.content['venue']['value'] == 'Submitted to TMLR'
        assert note.content['venueid']['value'] == 'TMLR/Submitted'
        assert note.content['supplementary_material']['value'] == '/attachment/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz.zip'
        assert note.content['supplementary_material']['readers'] == ["TMLR", "TMLR/Paper1/Action_Editors", "TMLR/Paper1/Reviewers", "TMLR/Paper1/Authors"]
        assert note.content['authorids']['value'] == ['~SomeFirstName_User1', '~Melissa_Eight1', '~Andrew_McCallumm1']
        assert note.content['authorids']['readers'] == ['TMLR', 'TMLR/Paper1/Action_Editors', 'TMLR/Paper1/Authors']

        author_group=openreview_client.get_group(f"{venue_id}/Paper1/Authors")
        assert author_group
        assert author_group.members == ['~SomeFirstName_User1', '~Melissa_Eight1', '~Andrew_McCallumm1']

        ## Post the submission 2
        submission_note_2 = test_client.post_note_edit(invitation='TMLR/-/Submission',
                                    signatures=['~SomeFirstName_User1'],
                                    note=Note(
                                        content={
                                            'title': { 'value': 'Paper title 2' },
                                            'abstract': { 'value': 'Paper abstract 2' },
                                            'authors': { 'value': ['SomeFirstName User', 'Celeste Martinez']},
                                            'authorids': { 'value': ['~SomeFirstName_User1', '~Celeste_Ana_Martinez1']},
                                            'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                                            'human_subjects_reporting': { 'value': 'Not applicable'},
                                            'pdf': { 'value': '/pdf/22234qweoiuweroi22234qweoiuweroi12345678.pdf' },
                                            'submission_length': { 'value': 'Regular submission (no more than 12 pages of main content)'}
                                        }
                                    ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_2['id'])
        note_id_2=submission_note_2['note']['id']

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        openreview_client.get_invitation('TMLR/Paper2/Action_Editors/-/Recommendation')

        author_group=openreview_client.get_group(f"{venue_id}/Paper2/Authors")
        assert author_group
        assert author_group.members == ['~SomeFirstName_User1', '~Celeste_Ana_Martinez1']
        assert openreview_client.get_group(f"{venue_id}/Paper2/Reviewers")
        assert openreview_client.get_group(f"{venue_id}/Paper2/Action_Editors")

        ## Post the submission 3
        submission_note_3 = test_client.post_note_edit(invitation='TMLR/-/Submission',
                                    signatures=['~SomeFirstName_User1'],
                                    note=Note(
                                        content={
                                            'title': { 'value': 'Paper title 3' },
                                            'abstract': { 'value': 'Paper abstract 3' },
                                            'authors': { 'value': ['SomeFirstName User', 'Andrew McCallum']},
                                            'authorids': { 'value': ['~SomeFirstName_User1', '~Andrew_McCallumm1']},
                                            'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                                            'human_subjects_reporting': { 'value': 'Not applicable'},
                                            'pdf': { 'value': '/pdf/22234qweoiuweroi22234qweoiuweroi12345678.pdf' },
                                            'submission_length': { 'value': 'Regular submission (no more than 12 pages of main content)'}
                                        }
                                    ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_3['id'])
        note_id_3=submission_note_3['note']['id']

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        openreview_client.get_invitation('TMLR/Paper3/Action_Editors/-/Recommendation')        

        author_group=openreview_client.get_group(f"{venue_id}/Paper3/Authors")
        assert author_group
        assert author_group.members == ['~SomeFirstName_User1', '~Andrew_McCallumm1']
        assert openreview_client.get_group(f"{venue_id}/Paper3/Reviewers")
        assert openreview_client.get_group(f"{venue_id}/Paper3/Action_Editors")

        editor_in_chief_group_id = f"{venue_id}/Editors_In_Chief"
        action_editors_id=f'{venue_id}/Action_Editors'

        # Assign Action Editor and immediately remove  assignment
        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_1,
            tail='~Joelle_Pineau1',
            weight=1
        ))

        paper_assignment_edge.ddate = openreview.tools.datetime_millis(datetime.datetime.now())
        paper_assignment_edge = raia_client.post_edge(paper_assignment_edge)

        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Assignment to new TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 0

        # Assign Action Editor
        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_1,
            tail='~Joelle_Pineau1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ae_group = raia_client.get_group(f'{venue_id}/Paper1/Action_Editors')
        assert ae_group.members == ['~Joelle_Pineau1']

        note = joelle_client.get_note(note_id_1)
        assert note
        assert note.content['assigned_action_editor']['value'] == '~Joelle_Pineau1'        

        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Assignment to new TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Joelle Pineau,

With this email, we request that you manage the review process for a new TMLR submission "1: Paper title UPDATED".

As a reminder, TMLR Action Editors (AEs) are **expected to accept all AE requests** to manage submissions that fall within your expertise and quota. Reasonable exceptions are 1) situations where exceptional personal circumstances (e.g. vacation, health problems) render you incapable of fully performing your AE duties or 2) you have a conflict of interest with one of the authors. If any such exception applies to you, contact us at tmlr@jmlr.org.

Your first task is to make sure the submitted preprint is appropriate for TMLR and respects our submission guidelines. Clear cases of desk rejection include submissions that are not anonymized, submissions that do not use the unmodified TMLR stylefile and submissions that clearly overlap with work already published in proceedings (or currently under review for publication). If you suspect but are unsure about whether a submission might need to be desk rejected for any other reasons (e.g. lack of fit with the scope of TMLR or lack of technical depth), please email us.

Please follow this link to perform this task: https://openreview.net/forum?id={note_id_1}&invitationId=TMLR/Paper1/-/Review_Approval

If you think the submission can continue through TMLR's review process, click the button "Under Review". Otherwise, click on "Desk Reject". Once the submission has been confirmed, then the review process will begin, and your next step will be to assign 3 reviewers to the paper. You will get a follow up email when OpenReview is ready for you to assign these 3 reviewers.

We thank you for your essential contribution to TMLR!

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        ## Try to assign the same AE again and get an error
        with pytest.raises(openreview.OpenReviewException, match=r'The maximum number \(1\) of Edges between .* and ~Joelle_Pineau1 has been reached'):
            paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
                readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
                writers=[venue_id, editor_in_chief_group_id],
                signatures=[editor_in_chief_group_id],
                head=note_id_1,
                tail='~Joelle_Pineau1',
                weight=1
            ))

        ## Check action editor recommendation is expired
        invitation = openreview_client.get_invitation(id='TMLR/Paper1/Action_Editors/-/Recommendation')
        assert invitation.expdate is not None
        assert invitation.expdate < openreview.tools.datetime_millis(datetime.datetime.now())
        assert openreview_client.get_invitation('TMLR/Paper1/-/Review_Approval')

        joelle_paper1_anon_groups = joelle_client.get_groups(prefix=f'{venue_id}/Paper1/Action_Editor_.*', signatory='~Joelle_Pineau1')
        assert len(joelle_paper1_anon_groups) == 1
        joelle_paper1_anon_group = joelle_paper1_anon_groups[0]        

        ## Make a comment before approving the submission to be under review
        comment_note_edit = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Official_Comment',
            signatures=[joelle_paper1_anon_group.id],
            note=Note(
                signatures=[joelle_paper1_anon_group.id],
                readers=['TMLR/Editors_In_Chief', 'TMLR/Paper1/Action_Editors'],
                forum=note_id_1,
                replyto=note_id_1,
                content={
                    'comment': { 'value': 'I\'m not sure if I should accept this paper to be under review' }
                }
            )
        )

        comment_edits = openreview_client.get_note_edits(note_id=comment_note_edit['note']['id'])
        assert len(comment_edits) == 1
        new_comment = 'This is an updated comment!'
        comment_edit = comment_edits[0]
        comment_edit.note.content['comment']['value'] = new_comment

        error_message = f'User is not writer of the Edit {comment_edit.id}'
        with pytest.raises(openreview.OpenReviewException, match=error_message):
            joelle_client.post_edit(comment_edit)
        
        ## Accept the submission 1
        under_review_note = joelle_client.post_note_edit(invitation= 'TMLR/Paper1/-/Review_Approval',
                                    signatures=[joelle_paper1_anon_group.id],
                                    note=Note(content={
                                        'under_review': { 'value': 'Appropriate for Review' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=under_review_note['id'])

        note = joelle_client.get_note(note_id_1)
        assert note
        assert note.odate
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/Paper1/-/Revision', 'TMLR/-/Edit', 'TMLR/-/Under_Review']
        assert note.readers == ['everyone']
        assert note.writers == ['TMLR', 'TMLR/Paper1/Authors']
        assert note.signatures == ['TMLR/Paper1/Authors']
        assert note.content['authorids']['value'] == ['~SomeFirstName_User1', '~Melissa_Eight1', '~Andrew_McCallumm1']
        assert note.content['venue']['value'] == 'Under review for TMLR'
        assert note.content['venueid']['value'] == 'TMLR/Under_Review'
        assert note.content['assigned_action_editor']['value'] == '~Joelle_Pineau1'
        assert note.content['_bibtex']['value'] == '''@article{
anonymous''' + str(datetime.datetime.fromtimestamp(note.cdate/1000).year) + '''paper,
title={Paper title {UPDATED}},
author={Anonymous},
journal={Submitted to Transactions on Machine Learning Research},
year={''' + str(datetime.datetime.today().year) + '''},
url={https://openreview.net/forum?id=''' + note_id_1 + '''},
note={Under review}
}'''

        edits = openreview_client.get_note_edits(note.id, invitation='TMLR/-/Under_Review')
        helpers.await_queue_edit(openreview_client, edit_id=edits[0].id)

        ## Check the edit history is public
        #edits = openreview_client.get_note_edits(note.id, invitation='TMLR/Paper1/-/Revision', sort='tcdate:asc')
        edits = openreview_client.get_note_edits(note.id, sort='tmdate:asc')
        assert edits
        for edit in edits:
            assert 'everyone' in edit.readers

        ## Remove assertion, the process function may run faster in the new machines
        ## try to make an assignment before the scores were computed
        # with pytest.raises(openreview.OpenReviewException, match=r'Can not add assignment, invitation is not active yet.'):
        #     paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
        #         readers=[venue_id, f"{venue_id}/Paper1/Action_Editors", '~David_Belanger1'],
        #         nonreaders=[f"{venue_id}/Paper1/Authors"],
        #         writers=[venue_id, f"{venue_id}/Paper1/Action_Editors"],
        #         signatures=[joelle_paper1_anon_group.id],
        #         head=note_id_1,
        #         tail='~David_Belanger1',
        #         weight=1
        #     ))

        helpers.await_queue_edit(openreview_client, invitation='TMLR/-/Under_Review')

        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Perform reviewer assignments for TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Joelle Pineau,

With this email, we request that you assign 3 reviewers to your assigned TMLR submission "1: Paper title UPDATED". The assignments must be completed **within 1 week** ({(datetime.datetime.now() + datetime.timedelta(weeks = 1)).strftime("%b %d")}). To do so, please follow this link: https://openreview.net/group?id=TMLR/Action_Editors and click on "Edit Assignment" for that paper in your "Assigned Papers" console.

As a reminder, up to their annual quota of 6 reviews per year, reviewers are expected to review all assigned submissions that fall within their expertise. Acceptable exceptions are 1) if they have an unsubmitted review for another TMLR submission or 2) situations where exceptional personal circumstances (e.g. vacation, health problems) render them incapable of fully performing their reviewing duties.

Once assigned, reviewers will be asked to acknowledge on OpenReview their responsibility to review this submission. This acknowledgement will be made visible to you on the OpenReview page of the submission. If the reviewer has not acknowledged their responsibility a couple of days after their assignment, consider reaching out to them directly to confirm.

We thank you for your essential contribution to TMLR!

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        ## Update submission 1 again
        updated_submission_note_1 = test_client.post_note_edit(invitation='TMLR/Paper1/-/Revision',
            signatures=['TMLR/Paper1/Authors'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title UPDATED' },
                    'supplementary_material': { 'value': '/attachment/' + 'z' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests VERSION 2'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'pdf': { 'value': '/pdf/22234qweoiuweroi22234qweoiuweroi12345678.pdf' },
                    'submission_length': { 'value': 'Regular submission (no more than 12 pages of main content)'}
                }
            ))
        helpers.await_queue_edit(openreview_client, edit_id=updated_submission_note_1['id'])

        note = openreview_client.get_note(note_id_1)
        assert note
        assert note.number == 1

        messages = openreview_client.get_messages(subject='[TMLR] Revision posted on submission 1: Paper title UPDATED')
        assert len(messages) == 7        

        ## Check active invitations
        invitations = joelle_client.get_invitations(replyForum=note_id_1)
        assert len(invitations) == 2
        assert f"{venue_id}/Paper1/-/Official_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Moderation" in [i.id for i in invitations]

        ## Assign Action editor to submission 2
        paper_assignment_edge_one = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Samy_Bengio1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_2,
            tail='~Samy_Bengio1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge_one.id)

        ## Assign another Action editor to submission 2
        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_2,
            tail='~Joelle_Pineau1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        time.sleep(5)

        # remove first assigned AE
        paper_assignment_edge_one.ddate = openreview.tools.datetime_millis(datetime.datetime.now())
        paper_assignment_edge_one = raia_client.post_edge(paper_assignment_edge_one)

        helpers.await_queue_edit(openreview_client, invitation='TMLR/Action_Editors/-/Assignment', count=6)

        # assert new AE is still assigned
        submission_two = raia_client.get_note(note_id_2)
        assert 'assigned_action_editor' in submission_two.content and submission_two.content['assigned_action_editor']['value'] == '~Joelle_Pineau1'

        joelle_paper2_anon_groups = joelle_client.get_groups(prefix=f'{venue_id}/Paper2/Action_Editor_.*', signatory='~Joelle_Pineau1')
        assert len(joelle_paper2_anon_groups) == 1
        joelle_paper2_anon_group = joelle_paper2_anon_groups[0]

        ## Desk reject the submission 2
        desk_reject_note = joelle_client.post_note_edit(invitation= 'TMLR/Paper2/-/Review_Approval',
                                    signatures=[joelle_paper2_anon_group.id],
                                    note=Note(content={
                                        'under_review': { 'value': 'Desk Reject' },
                                        'comment': { 'value': 'missing PDF' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=desk_reject_note['id'])

        assert openreview_client.get_invitation(f"{venue_id}/Paper2/-/Desk_Rejection_Approval")

        ## Check eic reminders
        openreview_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper2/-/Desk_Rejection_Approval',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 10)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 7)) + 2000,
                signatures=[venue_id]
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper2/-/Desk_Rejection_Approval-0-0')

        messages = journal.client.get_messages(subject = '[TMLR] You are late in performing a task for the paper 2: Paper title 2')
        assert len(messages) == 2

        messages = journal.client.get_messages(to='kyunghyun@mail.com', subject = '[TMLR] You are late in performing a task for the paper 2: Paper title 2')
        assert messages[0]['content']['text'] == f'''Hi Kyunghyun Cho,

Our records show that you are late on the current task:

Task: Desk Rejection Approval
Submission: Paper title 2
Number of days late: one week
Link: https://openreview.net/forum?id={note_id_2}

Please follow the provided link and complete your task ASAP.

We thank you for your cooperation.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        approval_note = raia_client.post_note_edit(invitation='TMLR/Paper2/-/Desk_Rejection_Approval',
                            signatures=[f"{venue_id}/Editors_In_Chief"],
                            note=Note(
                                signatures=[f"{venue_id}/Editors_In_Chief"],
                                forum=note_id_2,
                                replyto=desk_reject_note['note']['id'],
                                content= {
                                    'approval': { 'value': 'I approve the AE\'s decision.' }
                                 }
                            ))

        helpers.await_queue_edit(openreview_client, edit_id=approval_note['id'])

        messages = journal.client.get_messages(to = 'test@mail.com', subject = '[TMLR] Decision for your TMLR submission 2: Paper title 2')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi SomeFirstName User,

We are sorry to inform you that, after consideration by the assigned Action Editor, your TMLR submission "2: Paper title 2" has been rejected without further review.

Cases of desk rejection include submissions that are not anonymized, submissions that do not use the unmodified TMLR stylefile and submissions that clearly overlap with work already published in proceedings (or currently under review for publication).

To know more about the decision, please follow this link: https://openreview.net/forum?id={note_id_2}

For more details and guidelines on the TMLR review process, visit jmlr.org/tmlr.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        note = joelle_client.get_note(note_id_2)
        assert note
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/-/Edit', 'TMLR/-/Desk_Rejected']
        assert note.readers == ['TMLR', 'TMLR/Paper2/Action_Editors', 'TMLR/Paper2/Authors']
        assert note.writers == ['TMLR', 'TMLR/Paper2/Action_Editors']
        assert note.signatures == ['TMLR/Paper2/Authors']
        assert note.content['authorids']['value'] == ['~SomeFirstName_User1', '~Celeste_Ana_Martinez1']
        assert note.content['venue']['value'] == 'Desk rejected by TMLR'
        assert note.content['venueid']['value'] == 'TMLR/Desk_Rejected'

        ## Check invitations as an author
        invitations = test_client.get_invitations(replyForum=note_id_2)
        assert len(invitations) == 1
        assert invitations[0].id == 'TMLR/Paper2/-/Official_Comment'

        ## Check invitations as an AE
        invitations = joelle_client.get_invitations(replyForum=note_id_2)
        assert len(invitations) == 1
        assert invitations[0].id == 'TMLR/Paper2/-/Official_Comment'

        ## Check assignment invitations
        with pytest.raises(openreview.OpenReviewException, match=r'Can not edit assignments for this submission'):
            paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
                readers=[venue_id, editor_in_chief_group_id, '~Ryan_Adams1'],
                writers=[venue_id, editor_in_chief_group_id],
                signatures=[editor_in_chief_group_id],
                head=note_id_2,
                tail='~Ryan_Adams1',
                weight=1
            ))

        with pytest.raises(openreview.OpenReviewException, match=r'Can not edit assignments for this submission: TMLR/Desk_Rejected'):
            paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
                readers=[venue_id, f"{venue_id}/Paper2/Action_Editors", '~David_Belanger1'],
                nonreaders=[f"{venue_id}/Paper2/Authors"],
                writers=[venue_id, f"{venue_id}/Paper2/Action_Editors"],
                signatures=[joelle_paper2_anon_group.id],
                head=note_id_2,
                tail='~David_Belanger1',
                weight=1
            ))

        ## Withdraw the submission 3
        withdraw_note = test_client.post_note_edit(invitation='TMLR/Paper3/-/Withdrawal',
                                    signatures=[f'{venue_id}/Paper3/Authors'],
                                    note=Note(
                                        content={
                                            'withdrawal_confirmation': { 'value': 'I have read and agree with the venue\'s withdrawal policy on behalf of myself and my co-authors.' },
                                        }
                                    ))

        helpers.await_queue_edit(openreview_client, edit_id=withdraw_note['id'])

        note = test_client.get_note(note_id_3)
        assert note
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/-/Withdrawn']
        assert note.readers == ['TMLR', 'TMLR/Paper3/Action_Editors', 'TMLR/Paper3/Authors']
        assert note.writers == ['TMLR', 'TMLR/Paper3/Authors']
        assert note.signatures == ['TMLR/Paper3/Authors']
        assert note.content['authorids']['value'] == ['~SomeFirstName_User1', '~Andrew_McCallumm1']
        assert note.content['venue']['value'] == 'Withdrawn by Authors'
        assert note.content['venueid']['value'] == 'TMLR/Withdrawn_Submission'
        assert note.content['_bibtex']['value'] == '''@article{
anonymous''' + str(datetime.datetime.fromtimestamp(note.cdate/1000).year) + '''paper,
title={Paper title 3},
author={Anonymous},
journal={Submitted to Transactions on Machine Learning Research},
year={''' + str(datetime.datetime.today().year) + '''},
url={https://openreview.net/forum?id=''' + note_id_3 + '''},
note={Withdrawn}
}'''

        ## Check invitations
        invitations = openreview_client.get_invitations(replyForum=note_id_1)
        assert f"{venue_id}/Paper1/-/Withdrawal"  in [i.id for i in invitations]
        #TODO: fix tests
        #assert acceptance_invitation_id in [i.id for i in invitations]
        #assert reject_invitation_id in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Public_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Volunteer_to_Review" in [i.id for i in invitations]

        ## compute preferred emails
        openreview_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            signatures=['~Super_User1'],
            invitation=openreview.api.Invitation(
                id='TMLR/-/Preferred_Emails',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now()) + 2000,
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id='TMLR/-/Preferred_Emails-0-0', count=2)

        ## Check preferred emails
        assert openreview_client.get_edges_count(invitation='TMLR/-/Preferred_Emails') == 13

        ## David Belanger
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper1/Action_Editors", '~David_Belanger1'],
            nonreaders=[f"{venue_id}/Paper1/Authors"],
            writers=[venue_id, f"{venue_id}/Paper1/Action_Editors"],
            signatures=[joelle_paper1_anon_group.id],
            head=note_id_1,
            tail='~David_Belanger1',
            weight=1
        ))

        # immediately remove assignment of David Belanger
        paper_assignment_edge.ddate = openreview.tools.datetime_millis(datetime.datetime.now())
        paper_assignment_edge = joelle_client.post_edge(paper_assignment_edge)

        # wait for process function delay (5 seconds) and check no email is sent
        messages = journal.client.get_messages(
            to='david@mailone.com', subject='[TMLR] Assignment to review new TMLR submission Paper title UPDATED')
        assert len(messages) == 0

        # add David Belanger again
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper1/Action_Editors", '~David_Belanger1'],
            nonreaders=[f"{venue_id}/Paper1/Authors"],
            writers=[venue_id, f"{venue_id}/Paper1/Action_Editors"],
            signatures=[joelle_paper1_anon_group.id],
            head=note_id_1,
            tail='~David_Belanger1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)
        messages = journal.client.get_messages(to = 'david@mailone.com', subject = '[TMLR] Assignment to review new TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi David Belanger,

With this email, we request that you submit, within 2 weeks ({(datetime.datetime.now() + datetime.timedelta(weeks = 2)).strftime("%b %d")}) a review for your newly assigned TMLR submission "1: Paper title UPDATED". If the submission is longer than 12 pages (excluding any appendix), you may request more time to the AE.

Please acknowledge on OpenReview that you have received this review assignment by following this link: https://openreview.net/forum?id={note_id_1}&invitationId=TMLR/Paper1/Reviewers/-/~David_Belanger1/Assignment/Acknowledgement

As a reminder, reviewers are **expected to accept all assignments** for submissions that fall within their expertise and annual quota (6 papers). Acceptable exceptions are 1) if you have an active, unsubmitted review for another TMLR submission or 2) situations where exceptional personal circumstances (e.g. vacation, health problems) render you incapable of performing your reviewing duties. Based on the above, if you think you should not review this submission, contact your AE directly (you can do so by leaving a comment on OpenReview, with only the Action Editor as Reader).

To submit your review, please follow this link: https://openreview.net/forum?id={note_id_1}&invitationId=TMLR/Paper1/-/Review or check your tasks in the Reviewers Console: https://openreview.net/group?id=TMLR/Reviewers#reviewer-tasks

Once submitted, your review will become privately visible to the authors and AE. Then, as soon as 3 reviews have been submitted, all reviews will become publicly visible. For more details and guidelines on performing your review, visit jmlr.org/tmlr.

We thank you for your essential contribution to TMLR!

The TMLR Editors-in-Chief
note: replies to this email will go to the AE, Joelle Pineau.


Please note that responding to this email will direct your reply to joelle@mailseven.com.
'''
        assert messages[0]['content']['replyTo'] == 'joelle@mailseven.com'

        # remove assignment of David Belanger
        paper_assignment_edge.ddate = openreview.tools.datetime_millis(datetime.datetime.now())
        paper_assignment_edge = joelle_client.post_edge(paper_assignment_edge)

        # check that David Belanger has been removed from reviewer group
        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id, count=2)
        note = journal.client.get_note(note_id_1)
        group = journal.client.get_group('TMLR/Paper1/Reviewers')
        assert len(group.members) == 0

        # add David Belanger back
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper1/Action_Editors", '~David_Belanger1'],
            nonreaders=[f"{venue_id}/Paper1/Authors"],
            writers=[venue_id, f"{venue_id}/Paper1/Action_Editors"],
            signatures=[joelle_paper1_anon_group.id],
            head=note_id_1,
            tail='~David_Belanger1',
            weight=1
        ))

        forum_notes = journal.client.get_notes(invitation=journal.get_form_id(), content={ 'title': 'Acknowledgement of reviewer responsibility'})

        messages = journal.client.get_messages(to = 'david@mailone.com', subject = '[TMLR] Acknowledgement of Reviewer Responsibility')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi David Belanger,

TMLR operates somewhat differently to other journals and conferences. As a new reviewer, we'd like you to read and acknowledge some critical points of TMLR that might differ from your previous reviewing experience.

To perform this quick task, simply visit the following link: https://openreview.net/forum?id={forum_notes[0].id}&invitationId=TMLR/Reviewers/-/~David_Belanger1/Responsibility/Acknowledgement

We thank you for your essential contribution to TMLR!

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        ## Carlos Mondragon
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper1/Action_Editors", '~Carlos_Mondragon1'],
            nonreaders=[f"{venue_id}/Paper1/Authors"],
            writers=[venue_id, f"{venue_id}/Paper1/Action_Editors"],
            signatures=[joelle_paper1_anon_group.id],
            head=note_id_1,
            tail='~Carlos_Mondragon1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        messages = journal.client.get_messages(to = 'carlos@mailthree.com', subject = '[TMLR] Assignment to review new TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Carlos Mondragon,

With this email, we request that you submit, within 2 weeks ({(datetime.datetime.now() + datetime.timedelta(weeks = 2)).strftime("%b %d")}) a review for your newly assigned TMLR submission "1: Paper title UPDATED". If the submission is longer than 12 pages (excluding any appendix), you may request more time to the AE.

Please acknowledge on OpenReview that you have received this review assignment by following this link: https://openreview.net/forum?id={note_id_1}&invitationId=TMLR/Paper1/Reviewers/-/~Carlos_Mondragon1/Assignment/Acknowledgement

As a reminder, reviewers are **expected to accept all assignments** for submissions that fall within their expertise and annual quota (6 papers). Acceptable exceptions are 1) if you have an active, unsubmitted review for another TMLR submission or 2) situations where exceptional personal circumstances (e.g. vacation, health problems) render you incapable of performing your reviewing duties. Based on the above, if you think you should not review this submission, contact your AE directly (you can do so by leaving a comment on OpenReview, with only the Action Editor as Reader).

To submit your review, please follow this link: https://openreview.net/forum?id={note_id_1}&invitationId=TMLR/Paper1/-/Review or check your tasks in the Reviewers Console: https://openreview.net/group?id=TMLR/Reviewers#reviewer-tasks

Once submitted, your review will become privately visible to the authors and AE. Then, as soon as 3 reviews have been submitted, all reviews will become publicly visible. For more details and guidelines on performing your review, visit jmlr.org/tmlr.

We thank you for your essential contribution to TMLR!

The TMLR Editors-in-Chief
note: replies to this email will go to the AE, Joelle Pineau.


Please note that responding to this email will direct your reply to joelle@mailseven.com.
'''
        
        ack_invitation = openreview_client.get_invitation(id=f'{venue_id}/Reviewers/-/~David_Belanger1/Responsibility/Acknowledgement')
        forum_id = ack_invitation.edit['note']['forum']

 ## Check responsibility ackowledgement reminder
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=ack_invitation.id,
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 10)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 1)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Reviewers/-/~David_Belanger1/Responsibility/Acknowledgement-0-0')

        messages = journal.client.get_messages(subject = '[TMLR] You are late in performing a task: Responsibility Acknowledgement')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi David Belanger,

Our records show that you are late on the current task:

Task: Responsibility Acknowledgement
Number of days late: 1
Link: https://openreview.net/forum?id={forum_id}

Please follow the provided link and complete your task ASAP.

We thank you for your cooperation.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        ## Check reviewer assignment reminders
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/Reviewers/-/Assignment',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 10)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 1)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/Reviewers/-/Assignment-0-0')

        messages = journal.client.get_messages(subject = '[TMLR] You are late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['to'] == 'joelle@mailseven.com'
        assert messages[0]['content']['text'] == f'''Hi Joelle Pineau,

Our records show that you are late on the current action editor task:

Task: Reviewer Assignment
Submission: Paper title UPDATED
Number of days late: 1
Link: https://openreview.net/group?id=TMLR/Action_Editors#action-editor-tasks

Please follow the provided link and complete your task ASAP.

We thank you for your cooperation.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''


        ## Javier Burroni
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper1/Action_Editors", '~Javier_Burroni1'],
            nonreaders=[f"{venue_id}/Paper1/Authors"],
            writers=[venue_id, f"{venue_id}/Paper1/Action_Editors"],
            signatures=[joelle_paper1_anon_group.id],
            head=note_id_1,
            tail='~Javier_Burroni1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        messages = journal.client.get_messages(to = 'javier@mailtwo.com', subject = '[TMLR] Assignment to review new TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Javier Burroni,

With this email, we request that you submit, within 2 weeks ({(datetime.datetime.now() + datetime.timedelta(weeks = 2)).strftime("%b %d")}) a review for your newly assigned TMLR submission "1: Paper title UPDATED". If the submission is longer than 12 pages (excluding any appendix), you may request more time to the AE.

Please acknowledge on OpenReview that you have received this review assignment by following this link: https://openreview.net/forum?id={note_id_1}&invitationId=TMLR/Paper1/Reviewers/-/~Javier_Burroni1/Assignment/Acknowledgement

As a reminder, reviewers are **expected to accept all assignments** for submissions that fall within their expertise and annual quota (6 papers). Acceptable exceptions are 1) if you have an active, unsubmitted review for another TMLR submission or 2) situations where exceptional personal circumstances (e.g. vacation, health problems) render you incapable of performing your reviewing duties. Based on the above, if you think you should not review this submission, contact your AE directly (you can do so by leaving a comment on OpenReview, with only the Action Editor as Reader).

To submit your review, please follow this link: https://openreview.net/forum?id={note_id_1}&invitationId=TMLR/Paper1/-/Review or check your tasks in the Reviewers Console: https://openreview.net/group?id=TMLR/Reviewers#reviewer-tasks

Once submitted, your review will become privately visible to the authors and AE. Then, as soon as 3 reviews have been submitted, all reviews will become publicly visible. For more details and guidelines on performing your review, visit jmlr.org/tmlr.

We thank you for your essential contribution to TMLR!

The TMLR Editors-in-Chief
note: replies to this email will go to the AE, Joelle Pineau.


Please note that responding to this email will direct your reply to joelle@mailseven.com.
'''

        reviewerrs_group = raia_client.get_group(f'{venue_id}/Paper1/Reviewers')
        assert reviewerrs_group.members == ['~David_Belanger1', '~Carlos_Mondragon1', '~Javier_Burroni1']

        ## Add a fourth reviewer with an email address
        raia_client.add_members_to_group('TMLR/Reviewers', 'antony@irobot.com')
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper1/Action_Editors", 'antony@irobot.com'],
            nonreaders=[f"{venue_id}/Paper1/Authors"],
            writers=[venue_id, f"{venue_id}/Paper1/Action_Editors"],
            signatures=[joelle_paper1_anon_group.id],
            head=note_id_1,
            tail='antony@irobot.com',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ## Create the user
        helpers.create_user('antony@irobot.com', 'Antony', 'Bal')
        antony_client = OpenReviewClient(username='antony@irobot.com', password=helpers.strong_password)

        david_anon_groups=david_client.get_groups(prefix=f'{venue_id}/Paper1/Reviewer_.*', signatory='~David_Belanger1')
        assert len(david_anon_groups) == 1

        ## Send a reminder signed by the AE
        joelle_client.post_message(
            invitation='TMLR/Paper1/-/Message',
            signature='~Joelle_Pineau1',
            subject='TMLR Reminder to reviewers', 
            recipients=[david_anon_groups[0].id],
            message='This is a reminder to submit your reviews for TMLR Paper 1.'
        )

        messages = journal.client.get_messages(to = 'david@mailone.com', subject = 'TMLR Reminder to reviewers')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == 'This is a reminder to submit your reviews for TMLR Paper 1.\n\nThis message was signed by Joelle Pineau\n'        

        edges = david_client.get_grouped_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', groupby='weight')
        assert len(edges) == 1
        assert edges[0]['values'][0]['weight'] == 1

        ## Post a review edit
        david_review_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Review',
            signatures=[david_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' },
                    'additional_comments': { 'value': 'additional_comments' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'])

        edges = david_client.get_grouped_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', groupby='weight')
        assert len(edges) == 1
        assert edges[0]['values'][0]['weight'] == 1

        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'], process_index=0)
        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'], process_index=1)

        edges = david_client.get_grouped_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', groupby='weight')
        assert len(edges) == 1
        assert edges[0]['values'][0]['weight'] == 0

        ## Check invitations as a reviewer
        invitations = david_client.get_invitations(replyForum=note_id_1)
        assert len(invitations) == 2
        assert f"{venue_id}/Paper1/-/Review"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Comment"  in [i.id for i in invitations]

        ## Check invitations
        invitations = openreview_client.get_invitations(replyForum=note_id_1)
        assert f"{venue_id}/Paper1/-/Revision"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Withdrawal"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Volunteer_to_Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Public_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Moderation" in [i.id for i in invitations]

        ## Post an official comment from the authors
        comment_note = test_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Official_Comment',
            signatures=[f"{venue_id}/Paper1/Authors"],
            note=Note(
                signatures=[f"{venue_id}/Paper1/Authors"],
                readers=['TMLR/Editors_In_Chief', 'TMLR/Paper1/Action_Editors', david_anon_groups[0].id, 'TMLR/Paper1/Authors'],
                forum=note_id_1,
                replyto=david_review_note['note']['id'],
                content={
                    'title': { 'value': 'Thanks for your review' },
                    'comment': { 'value': 'This is helpfull feedback' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=comment_note['id'])

        messages = journal.client.get_messages(subject = '[TMLR] Official Comment posted on submission 1: Paper title UPDATED')
        assert len(messages) == 8

        ## Post an official comment from the reviewer
        comment_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Official_Comment',
            signatures=[david_anon_groups[0].id],
            note=Note(
                signatures=[david_anon_groups[0].id],
                readers=['TMLR/Editors_In_Chief', 'TMLR/Paper1/Action_Editors', david_anon_groups[0].id, 'TMLR/Paper1/Authors'],
                forum=note_id_1,
                replyto=comment_note['note']['id'],
                content={
                    'title': { 'value': 'I updated the review' },
                    'comment': { 'value': 'Thanks for the response, I updated the review.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=comment_note['id'])

        ## Poster a comment without EIC as readers
        with pytest.raises(openreview.OpenReviewException, match=r'Editors In Chief must be readers of the comment'):
            comment_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Official_Comment',
                signatures=[david_anon_groups[0].id],
                note=Note(
                    signatures=[david_anon_groups[0].id],
                    readers=['TMLR/Paper1/Action_Editors', david_anon_groups[0].id],
                    forum=note_id_1,
                    replyto=note_id_1,
                    content={
                        'title': { 'value': 'Contact AE' },
                        'comment': { 'value': 'I want to contact the AE.' }
                    }
                )
            )

        ## Post an official comment from the reviewer to the EIC only
        comment_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Official_Comment',
            signatures=[david_anon_groups[0].id],
            note=Note(
                signatures=[david_anon_groups[0].id],
                readers=['TMLR/Editors_In_Chief', david_anon_groups[0].id],
                forum=note_id_1,
                replyto=comment_note['note']['id'],
                content={
                    'title': { 'value': 'I have a conflict with this paper' },
                    'comment': { 'value': 'I know the authors and I can not review this paper.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=comment_note['id'])

        messages = journal.client.get_messages(to='raia@mail.com', subject = '[TMLR] Official Comment posted on submission 1: Paper title UPDATED')
        assert len(messages) == 2
        assert messages[-1]['content']['text'] == f'''Hi Raia Hadsell,

An official comment has been posted on a submission for which you are serving as Editor-In-Chief.

Submission: Paper title UPDATED
Title: I have a conflict with this paper
Comment: I know the authors and I can not review this paper.

To view the official comment, click here: https://openreview.net/forum?id={note_id_1}&noteId={comment_note['note']['id']}


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        ## Post an official comment from the EIC to the EIC only
        comment_note = raia_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Official_Comment',
            signatures=['TMLR/Editors_In_Chief'],
            note=Note(
                signatures=['TMLR/Editors_In_Chief'],
                readers=['TMLR/Editors_In_Chief'],
                forum=note_id_1,
                replyto=note_id_1,
                content={
                    'title': { 'value': 'Do not approve this yet' },
                    'comment': { 'value': 'pending moderation, please do not approve.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=comment_note['id'])

        messages = journal.client.get_messages(to='raia@mail.com', subject = '[TMLR] Official Comment posted on submission 1: Paper title UPDATED')
        assert len(messages) == 2

        # Post a public comment
        comment_note = peter_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Public_Comment',
            signatures=['~Peter_Snow1'],
            note=Note(
                signatures=['~Peter_Snow1'],
                forum=note_id_1,
                replyto=note_id_1,
                content={
                    'title': { 'value': 'Comment title' },
                    'comment': { 'value': 'This is an inapropiate comment' }
                }
            )
        )
        comment_note_id=comment_note['note']['id']
        note = guest_client.get_note(comment_note_id)
        assert note
        assert note.invitations == ['TMLR/Paper1/-/Public_Comment']
        assert note.readers == ['everyone']
        assert note.writers == ['TMLR', 'TMLR/Paper1/Action_Editors', '~Peter_Snow1']
        assert note.signatures == ['~Peter_Snow1']
        assert note.content['title']['value'] == 'Comment title'
        assert note.content['comment']['value'] == 'This is an inapropiate comment'

        helpers.await_queue_edit(openreview_client, edit_id=comment_note['id'])

        messages = journal.client.get_messages(subject = '[TMLR] Public Comment posted on submission 1: Paper title UPDATED')
        assert len(messages) == 9
        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Public Comment posted on submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['to'] == 'joelle@mailseven.com'
        assert messages[0]['content']['text'] == f'''Hi Joelle Pineau,

A public comment has been posted on a submission for which you are an Action Editor.

Submission: Paper title UPDATED
Title: Comment title
Comment: This is an inapropiate comment

To view the public comment, click here: https://openreview.net/forum?id={note_id_1}&noteId={comment_note_id}


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''


        # Moderate a public comment
        moderated_comment_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Moderation',
            signatures=[joelle_paper1_anon_group.id],
            note=Note(
                id=comment_note_id,
                content={
                    'title': { 'value': 'Moderated comment' },
                    'comment': { 'value': 'Moderated content' }
                }
            )
        )

        note = joelle_client.get_note(comment_note_id)
        assert note
        assert note.invitations == ['TMLR/Paper1/-/Public_Comment', 'TMLR/Paper1/-/Moderation']
        assert note.readers == ['everyone']
        assert note.writers == ['TMLR', 'TMLR/Paper1/Action_Editors']
        assert note.signatures == ['~Peter_Snow1']
        assert note.content.get('title').get('value') == 'Moderated comment'
        assert note.content.get('comment').get('value') == 'Moderated content'

        ## Assign two more reviewers
        javier_anon_groups=javier_client.get_groups(prefix=f'{venue_id}/Paper1/Reviewer_.*', signatory='~Javier_Burroni1')
        assert len(javier_anon_groups) == 1

        ## Post a review edit
        javier_review_note = javier_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Review',
            signatures=[javier_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'])

        ## Check invitations
        invitations = openreview_client.get_invitations(replyForum=note_id_1)
        assert f"{venue_id}/Paper1/-/Revision"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Withdrawal"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Volunteer_to_Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Public_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Moderation" in [i.id for i in invitations]


        ## Poster another review with the same signature and get an error
        with pytest.raises(openreview.OpenReviewException, match=r'You have reached the maximum number \(1\) of replies for this Invitation'):
            review_note = javier_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Review',
                signatures=[javier_anon_groups[0].id],
                note=Note(
                    content={
                        'summary_of_contributions': { 'value': 'summary_of_contributions' },
                        'claims_and_evidence': { 'value': 'Yes' },
                        'claims_explanation': { 'value': 'claims_explanation' },
                        'audience': { 'value': 'Yes' },
                        'audience_explanation': { 'value': 'audience_explanation' },
                        'requested_changes': { 'value': 'requested_changes' },
                        'broader_impact_concerns': { 'value': 'broader_impact_concerns' }                   
                    }
                )
            )

        reviews=openreview_client.get_notes(forum=note_id_1, invitation=f'{venue_id}/Paper1/-/Review', sort='number:desc')
        assert len(reviews) == 2
        assert reviews[0].readers == [f"{venue_id}/Editors_In_Chief", f"{venue_id}/Paper1/Action_Editors", javier_anon_groups[0].id, f"{venue_id}/Paper1/Authors"]
        assert reviews[1].readers == [f"{venue_id}/Editors_In_Chief", f"{venue_id}/Paper1/Action_Editors", david_anon_groups[0].id, f"{venue_id}/Paper1/Authors"]

        ## Check review reminders
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/-/Review',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 10)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 1)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/-/Review-0-0')

        messages = journal.client.get_messages(subject = '[TMLR] You are late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 3
        messages = journal.client.get_messages(to = 'carlos@mailthree.com', subject = '[TMLR] You are late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['to'] == 'carlos@mailthree.com'
        assert messages[0]['content']['text'] == f'''Hi Carlos Mondragon,

Our records show that you are late on the current reviewing task:

Task: Review
Submission: Paper title UPDATED
Number of days late: 1
Link: https://openreview.net/forum?id={note_id_1}


Please follow the provided link and complete your task ASAP.

We thank you for your cooperation.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to joelle@mailseven.com.
'''

        messages = journal.client.get_messages(subject = '[TMLR] Reviewer is late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 0

        ## Check review reminders
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/-/Review',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 10)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 7)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/-/Review-0-1')

        messages = journal.client.get_messages(subject = '[TMLR] You are late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 5

        messages = journal.client.get_messages(subject = '[TMLR] Reviewer is late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 2
        assert messages[0]['content']['to'] == 'joelle@mailseven.com'        
        assert any(message['content']['text'] == f'''Hi Joelle Pineau,

Our records show that a reviewer on a paper you are the AE for is *one week* late on a reviewing task:

Task: Review
Reviewer: Carlos Mondragon
Submission: Paper title UPDATED
Link: https://openreview.net/forum?id={note_id_1}

Please follow up directly with the reviewer in question to ensure they complete their task ASAP.

We thank you for your cooperation.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
''' for message in messages)

        ## Check review reminders
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/-/Review',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 20)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 14)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/-/Review-0-2')

        messages = journal.client.get_messages(subject = '[TMLR] You are late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 7

        messages = journal.client.get_messages(subject = '[TMLR] Reviewer is late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 4
        assert messages[-1]['content']['to'] == 'joelle@mailseven.com'
        assert any(message['content']['text'] == f'''Hi Joelle Pineau,

Our records show that a reviewer on a paper you are the AE for is *two weeks* late on a reviewing task:

Task: Review
Reviewer: Antony Bal
Submission: Paper title UPDATED
Link: https://openreview.net/forum?id={note_id_1}

Please follow up directly with the reviewer in question to ensure they complete their task ASAP.

We thank you for your cooperation.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
''' for message in messages)

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/-/Review-1-0')
        
        messages = journal.client.get_messages(subject = '[TMLR] Fewer than 3 ACKs for the paper 1: Paper title UPDATED')
        assert len(messages) == 2

        ## Check review reminders
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/-/Review',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 40)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 30)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/-/Review-0-3')

        messages = journal.client.get_messages(subject = '[TMLR] You are late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 9

        messages = journal.client.get_messages(subject = '[TMLR] Reviewer is late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 10

        messages = journal.client.get_messages(to= 'raia@mail.com', subject = '[TMLR] Reviewer is late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 2
        assert any(message['content']['text'] == f'''Hi Raia Hadsell,

Our records show that a reviewer is *one month* late on a reviewing task:

Task: Review
Reviewer: Carlos Mondragon
Submission: Paper title UPDATED
Link: https://openreview.net/forum?id={note_id_1}

OpenReview Team


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
''' for message in messages)

        messages = journal.client.get_messages(to= 'joelle@mailseven.com', subject = '[TMLR] Reviewer is late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 6
        assert any(message['content']['text'] == f'''Hi Joelle Pineau,

Our records show that a reviewer on a paper you are the AE for is *one month* late on a reviewing task:

Task: Review
Reviewer: Carlos Mondragon
Submission: Paper title UPDATED
Link: https://openreview.net/forum?id={note_id_1}

Please follow up directly with the reviewer in question to ensure they complete their task ASAP.

We thank you for your cooperation.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
''' for message in messages)


        ## Check reviewer assignment acknowledge reminders
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/Reviewers/-/~Carlos_Mondragon1/Assignment/Acknowledgement',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 10)),                                                 
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 1)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/Reviewers/-/~Carlos_Mondragon1/Assignment/Acknowledgement-0-0')

        messages = journal.client.get_messages(to = 'carlos@mailthree.com', subject = '[TMLR] You are late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 5
        assert any(message['content']['text'] == f'''Hi Carlos Mondragon,

Our records show that you have not acknowledged your TMLR assignment yet:

Task: Assignment Acknowledgement
Submission: Paper title UPDATED
Number of days late: 1
Link: https://openreview.net/forum?id={note_id_1}

Acknowledging review assignments allows AEs to receive a direct confirmation that you are aware of the assignment. As a reminder, reviewers in the TMLR pool are expected to perform all review assignments of submissions that fall within their expertise and quota (unless they are exceptionally temporarily unavailable due to reasons such as illness, vacation or work leave).
Please follow the provided link and complete your task ASAP.

We thank you for your cooperation.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to joelle@mailseven.com.
''' for message in messages)

        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/Reviewers/-/~Carlos_Mondragon1/Assignment/Acknowledgement',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 10)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 5)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/Reviewers/-/~Carlos_Mondragon1/Assignment/Acknowledgement-0-1')

        messages = journal.client.get_messages(to = 'carlos@mailthree.com', subject = '[TMLR] You are late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 6
        assert messages[5]['content']['text'] == f'''Hi Carlos Mondragon,

Our records show that you have not acknowledged your TMLR assignment yet:

Task: Assignment Acknowledgement
Submission: Paper title UPDATED
Number of days late: five days
Link: https://openreview.net/forum?id={note_id_1}

Acknowledging review assignments allows AEs to receive a direct confirmation that you are aware of the assignment. As a reminder, reviewers in the TMLR pool are expected to perform all review assignments of submissions that fall within their expertise and quota (unless they are exceptionally temporarily unavailable due to reasons such as illness, vacation or work leave).
Please follow the provided link and complete your task ASAP.

We thank you for your cooperation.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to joelle@mailseven.com.
'''

        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/Reviewers/-/~Carlos_Mondragon1/Assignment/Acknowledgement',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 20)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 12)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/Reviewers/-/~Carlos_Mondragon1/Assignment/Acknowledgement-0-2')

        messages = journal.client.get_messages(to = 'carlos@mailthree.com', subject = '[TMLR] You are late in performing a task for assigned paper 1: Paper title UPDATED')
        assert len(messages) == 7
        assert messages[6]['content']['text'] == f'''Hi Carlos Mondragon,

Our records show that you have not acknowledged your TMLR assignment yet:

Task: Assignment Acknowledgement
Submission: Paper title UPDATED
Number of days late: twelve days
Link: https://openreview.net/forum?id={note_id_1}

Acknowledging review assignments allows AEs to receive a direct confirmation that you are aware of the assignment. As a reminder, reviewers in the TMLR pool are expected to perform all review assignments of submissions that fall within their expertise and quota (unless they are exceptionally temporarily unavailable due to reasons such as illness, vacation or work leave).
Please follow the provided link and complete your task ASAP.

We thank you for your cooperation.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to joelle@mailseven.com.
'''

        late_reviewers = journal.get_late_invitees('TMLR/Paper1/Reviewers/-/~Carlos_Mondragon1/Assignment/Acknowledgement')
        assert late_reviewers
        assert '~Carlos_Mondragon1' in late_reviewers

        carlos_anon_groups=carlos_client.get_groups(prefix=f'{venue_id}/Paper1/Reviewer_.*', signatory='~Carlos_Mondragon1')
        assert len(carlos_anon_groups) == 1

        ## post the assignment ack
        formatted_date = (datetime.datetime.now() + datetime.timedelta(weeks = 2)).strftime("%b %d, %Y")
        assignment_ack_note = carlos_client.post_note_edit(invitation=f'TMLR/Paper1/Reviewers/-/~Carlos_Mondragon1/Assignment/Acknowledgement',
            signatures=[carlos_anon_groups[0].id],
            note=Note(
                content={
                    'assignment_acknowledgement': { 'value': f'I acknowledge my responsibility to submit a review for this submission by the end of day on {formatted_date} UTC time.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=assignment_ack_note['id'])

        late_reviewers = journal.get_late_invitees('TMLR/Paper1/Reviewers/-/~Carlos_Mondragon1/Assignment/Acknowledgement')
        assert not late_reviewers

        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Assignment Acknowledgement posted on submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Joelle Pineau,

Carlos Mondragon posted an assignment acknowledgement on a submission for which you are an Action Editor.

Submission: Paper title UPDATED
Assignment acknowledgement: I acknowledge my responsibility to submit a review for this submission by the end of day on {formatted_date} UTC time.

To view the acknowledgement, click here: https://openreview.net/forum?id={note_id_1}&noteId={assignment_ack_note['note']['id']}


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''



        ## Post a review edit
        carlos_review_note = carlos_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Review',
            signatures=[carlos_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'])

        ## Check invitations
        invitations = openreview_client.get_invitations(replyForum=note_id_1)
        assert f"{venue_id}/-/Under_Review"  in [i.id for i in invitations]
        assert f"{venue_id}/-/Desk_Rejected"  in [i.id for i in invitations]
        assert f"{venue_id}/-/Rejected"  in [i.id for i in invitations]
        assert f"{venue_id}/-/Withdrawn"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Revision"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Withdrawal" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Volunteer_to_Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Public_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Moderation" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Recommendation" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Review_Rating_Enabling" not in [i.id for i in invitations]

        ## All the reviewes should be public now
        reviews=openreview_client.get_notes(forum=note_id_1, invitation=f'{venue_id}/Paper1/-/Review', sort= 'number:asc')
        assert len(reviews) == 3
        assert reviews[0].readers == ['everyone']
        assert reviews[0].signatures == [david_anon_groups[0].id]
        assert reviews[1].readers == ['everyone']
        assert reviews[1].signatures == [javier_anon_groups[0].id]
        assert reviews[2].readers == ['everyone']
        assert reviews[2].signatures == [carlos_anon_groups[0].id]

        ## Reviewers should see other reviewer's identity
        anon_groups = carlos_client.get_groups(prefix=f'{venue_id}/Paper1/Reviewer_')
        assert len(anon_groups) == 4

        ## All the comments should be public now
        comments = openreview_client.get_notes(forum=note_id_1, invitation=f'{venue_id}/Paper1/-/Official_Comment', sort= 'number:asc')
        assert len(comments) == 5
        assert comments[0].readers != ['everyone']
        assert comments[1].readers == ['everyone']
        assert comments[2].readers == ['everyone']
        assert comments[3].readers != ['everyone']
        assert comments[4].readers != ['everyone']

        messages = openreview_client.get_messages(to = 'test@mail.com', subject = '[TMLR] Reviewer responses and discussion for your TMLR submission')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi SomeFirstName User,

Now that 3 reviews have been submitted for your submission  1: Paper title UPDATED, all reviews have been made public. If you haven't already, please read the reviews and start engaging with the reviewers to attempt to address any concern they may have about your submission.

You will have 2 weeks to interact with the reviewers, including uploading any revisions. To maximize the period of interaction and discussion, please respond as soon as possible. Additionally, revising the submission PDF in light of reviewer feedback is possible and encouraged (consider making changes in a different color to help reviewers), in order to give reviewers maximum confidence that their concerns are addressed. The reviewers will be using this time period to hear from you and gather all the information they need. In about 2 weeks ({(datetime.datetime.now() + datetime.timedelta(weeks = 2)).strftime("%b %d")}), and no later than 4 weeks ({(datetime.datetime.now() + datetime.timedelta(weeks = 4)).strftime("%b %d")}), reviewers will submit their formal decision recommendation to the Action Editor in charge of your submission.

Visit the following link to respond to the reviews: https://openreview.net/forum?id={note_id_1}

For more details and guidelines on the TMLR review process, visit jmlr.org/tmlr.

The TMLR Editors-in-Chief
note: replies to this email will go to the AE, Joelle Pineau.


Please note that responding to this email will direct your reply to joelle@mailseven.com.
'''
        assert messages[0]['content']['replyTo'] == 'joelle@mailseven.com'

        messages = openreview_client.get_messages(to = 'carlos@mailthree.com', subject = '[TMLR] Start of author discussion for TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Carlos Mondragon,

There are now 3 reviews that have been submitted for your assigned submission "1: Paper title UPDATED" and all reviews have been made public. Please read the other reviews and start engaging with the authors (and possibly the other reviewers and AE) in order to address any concern you may have about the submission. Your goal should be to gather all the information you need **within the next 2 weeks** to be comfortable submitting a decision recommendation for this paper. You will receive an upcoming notification on how to enter your recommendation in OpenReview.

You will find the OpenReview page for this submission at this link: https://openreview.net/forum?id={note_id_1}

For more details and guidelines on the TMLR review process, visit jmlr.org/tmlr.

We thank you for your essential contribution to TMLR!

The TMLR Editors-in-Chief
note: replies to this email will go to the AE, Joelle Pineau.


Please note that responding to this email will direct your reply to joelle@mailseven.com.
'''

        messages = openreview_client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Start of author discussion for TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Joelle Pineau,

Now that 3 reviews have been submitted for submission 1: Paper title UPDATED, all reviews have been made public and authors and reviewers have been notified that the discussion phase has begun. Please read the reviews and oversee the discussion between the reviewers and the authors. The goal of the reviewers should be to gather all the information they need to be comfortable submitting a decision recommendation to you for this submission. Reviewers will be able to submit their formal decision recommendation starting in **2 weeks**.

You will find the OpenReview page for this submission at this link: https://openreview.net/forum?id={note_id_1}

For more details and guidelines on the TMLR review process, visit jmlr.org/tmlr.

We thank you for your essential contribution to TMLR!

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        messages = openreview_client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Too many reviewers assigned to TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Joelle Pineau,

It appears that, while submission 1: Paper title UPDATED now has its minimum of 3 reviews submitted, there are some additional assigned reviewers who have pending reviews. This may be because you had assigned additional emergency reviewers, e.g. because some of the initially assigned reviewers were late or unresponsive. If that is the case, or generally if these additional reviews are no longer needed, please unassign the extra reviewers and let them know that their review is no longer needed.

Additionally, if any extra reviewer corresponds to a reviewer who was unresponsive, please consider submitting a reviewer report, so we can track such undesirable behavior. You can submit a report through link \"Reviewers Report\" at the top of your AE console.

For more details and guidelines on the TMLR review process, visit jmlr.org/tmlr.

We thank you for your essential contribution to TMLR!

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''
        
        ## Update submission 1 again
        updated_submission_note_1 = test_client.post_note_edit(invitation='TMLR/Paper1/-/Revision',
            signatures=['TMLR/Paper1/Authors'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title UPDATED' },
                    'supplementary_material': { 'value': '/attachment/' + 'z' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests VERSION 3'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'pdf': { 'value': '/pdf/22234qweoiuweroi22234qweoiuweroi12345678.pdf' },
                    'submission_length': { 'value': 'Regular submission (no more than 12 pages of main content)'}
                }
            ))
        helpers.await_queue_edit(openreview_client, edit_id=updated_submission_note_1['id'])

        messages = openreview_client.get_messages(subject='[TMLR] Revision posted on submission 1: Paper title UPDATED')
        assert len(messages) == 15        

        ## Edit a review and don't release the review again
        review_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Review',
            signatures=[david_anon_groups[0].id],
            note=Note(
                id=david_review_note['note']['id'],
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions V2' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation V2' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation V2' },
                    'requested_changes': { 'value': 'requested_changes V2' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns V2' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=review_note['id'])

        messages = openreview_client.get_messages(to = 'test@mail.com', subject = '[TMLR] Reviewer responses and discussion for your TMLR submission')
        assert len(messages) == 1


        ## Assign reviewer 4
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper1/Action_Editors", '~Hugo_Larochelle1'],
            nonreaders=[f"{venue_id}/Paper1/Authors"],
            writers=[venue_id, f"{venue_id}/Paper1/Action_Editors"],
            signatures=[joelle_paper1_anon_group.id],
            head=note_id_1,
            tail='~Hugo_Larochelle1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        hugo_anon_groups=hugo_client.get_groups(prefix=f'{venue_id}/Paper1/Reviewer_.*', signatory='~Hugo_Larochelle1')
        assert len(hugo_anon_groups) == 1

        ## Post a review edit
        hugo_review_note = hugo_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Review',
            signatures=[hugo_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=hugo_review_note['id'])

        ## All the reviews should be public now
        reviews=openreview_client.get_notes(forum=note_id_1, invitation=f'{venue_id}/Paper1/-/Review', sort= 'number:asc')
        assert len(reviews) == 4
        assert reviews[0].readers == ['everyone']
        assert reviews[0].signatures == [david_anon_groups[0].id]
        assert reviews[1].readers == ['everyone']
        assert reviews[1].signatures == [javier_anon_groups[0].id]
        assert reviews[2].readers == ['everyone']
        assert reviews[2].signatures == [carlos_anon_groups[0].id]
        assert reviews[3].readers == ['everyone']
        assert reviews[3].signatures == [hugo_anon_groups[0].id]

        invitation = raia_client.get_invitation(f'{venue_id}/Paper1/-/Official_Recommendation')
        assert invitation.cdate > openreview.tools.datetime_millis(datetime.datetime.now())
        assert invitation.edit['note']['content']['certification_recommendations']['value']['param']['enum'] == ['Featured Certification', 'Reproducibility Certification', 'Survey Certification']

        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/-/Official_Recommendation',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now()) + 1000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        time.sleep(5) ## wait until the process function runs

        ## Check emails being sent to Reviewers and AE
        messages = journal.client.get_messages(subject = '[TMLR] Submit official recommendation for TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 5
        messages = journal.client.get_messages(to= 'hugo@mailsix.com', subject = '[TMLR] Submit official recommendation for TMLR submission 1: Paper title UPDATED')
        assert messages[0]['content']['text'] == f'''Hi Hugo Larochelle,

Thank you for submitting your review and engaging with the authors of TMLR submission "1: Paper title UPDATED".

You may now submit your official recommendation for the submission. Before doing so, make sure you have sufficiently discussed with the authors (and possibly the other reviewers and AE) any concerns you may have about the submission.

We ask that you submit your recommendation within 2 weeks ({(datetime.datetime.now() + datetime.timedelta(weeks = 4)).strftime("%b %d")}). To do so, please follow this link: https://openreview.net/forum?id={note_id_1}&invitationId=TMLR/Paper1/-/Official_Recommendation

For more details and guidelines on performing your review, visit jmlr.org/tmlr.

We thank you for your essential contribution to TMLR!

The TMLR Editors-in-Chief
note: replies to this email will go to the AE, Joelle Pineau.


Please note that responding to this email will direct your reply to joelle@mailseven.com.
'''
        messages = journal.client.get_messages(subject = '[TMLR] Reviewers must submit official recommendation for TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 1

        messages = openreview_client.get_messages(to = 'test@mail.com', subject = '[TMLR] Discussion period ended for TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 0

        antony_anon_groups=antony_client.get_groups(prefix=f'{venue_id}/Paper1/Reviewer_.*', signatory='~Antony_Bal1')
        assert len(antony_anon_groups) == 1

        # try to post official recommendation before review
        with pytest.raises(openreview.OpenReviewException, match=r'You must submit your official review before submitting your recommendation'):
            official_recommendation_note = antony_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Official_Recommendation',
                signatures=[antony_anon_groups[0].id],
                note=Note(
                    content={
                        'decision_recommendation': { 'value': 'Leaning Accept' },
                        'claims_and_evidence': { 'value': 'Yes' },
                        'audience': { 'value': 'Yes' },
                        'recommendation_to_iclr_track': { 'value': 'Weakly Recommend' },
                        'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because I like it.' }
                    }
                )
            )

        ## Post a review edit
        antony_review_note = antony_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Review',
            signatures=[antony_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=antony_review_note['id'])

        ## Post a review recommendation
        official_recommendation_note = carlos_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Official_Recommendation',
            signatures=[carlos_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Accept' },
                    'certification_recommendations': { 'value': ['Featured Certification'] },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        ## Check invitations
        invitations = openreview_client.get_invitations(replyForum=note_id_1)
        assert f"{venue_id}/Paper1/-/Revision"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Withdrawal"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Volunteer_to_Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Public_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Moderation" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Recommendation" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Review_Rating_Enabling" in [i.id for i in invitations]

        official_recommendation_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Official_Recommendation',
            signatures=[david_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Accept' },
                    'certification_recommendations': { 'value': ['Featured Certification', 'Reproducibility Certification'] },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        ## Check invitations
        invitations = openreview_client.get_invitations(replyForum=note_id_1)
        assert f"{venue_id}/Paper1/-/Revision"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Withdrawal"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Volunteer_to_Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Public_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Moderation" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Recommendation" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Review_Rating_Enabling" in [i.id for i in invitations]

        official_recommendation_note = javier_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Official_Recommendation',
            signatures=[javier_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Accept' },
                    'certification_recommendations': { 'value': ['Survey Certification'] },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        antony_official_recommendation_note = antony_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Official_Recommendation',
            signatures=[antony_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Accept' },
                    'certification_recommendations': { 'value': ['Survey Certification'] },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=antony_official_recommendation_note['id'])

        ## Check invitations
        invitations = openreview_client.get_invitations(replyForum=note_id_1)
        assert f"{venue_id}/Paper1/-/Revision"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Withdrawal"  in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Volunteer_to_Review" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Public_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Moderation" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Official_Recommendation" in [i.id for i in invitations]
        assert f"{david_anon_groups[0].id}/-/Rating" in [i.id for i in invitations]
        assert f"{javier_anon_groups[0].id}/-/Rating" in [i.id for i in invitations]
        assert f"{carlos_anon_groups[0].id}/-/Rating" in [i.id for i in invitations]
        assert f"{hugo_anon_groups[0].id}/-/Rating" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Review_Rating_Enabling" not in [i.id for i in invitations]


        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Evaluate reviewers and submit decision for TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Joelle Pineau,

Thank you for overseeing the review process for TMLR submission "1: Paper title UPDATED".

All reviewers have submitted their official recommendation of a decision for the submission. Therefore it is now time for you to determine a decision for the submission. Before doing so:

- Make sure you have sufficiently discussed with the authors (and possibly the reviewers) any concern you may have about the submission.
- Rate the quality of the reviews submitted by the reviewers. **You will not be able to submit your decision until these ratings have been submitted**. To rate a review, go on the submission's page and click on button "Rating" for each of the reviews.

We ask that you submit your decision **within 1 week** ({(datetime.datetime.now() + datetime.timedelta(weeks = 1)).strftime("%b %d")}). To do so, please follow this link: https://openreview.net/forum?id={note_id_1}&invitationId=TMLR/Paper1/-/Decision

The possible decisions are:
- **Accept as is**: once its camera ready version is submitted, the manuscript will be marked as accepted.
- **Accept with minor revision**: to use if you wish to request some specific revisions to the manuscript, to be specified explicitly in your decision comments. These revisions will be expected from the authors when they submit their camera ready version.
- **Reject**: the paper is rejected, but you may indicate whether you would be willing to consider a significantly revised version of the manuscript. Such a revised submission will need to be entered as a new submission, that will also provide a link to this rejected submission as well as a description of the changes made since.

Your decision may also include certification(s) recommendations for the submission (in case of an acceptance).

For more details and guidelines on performing your review, visit jmlr.org/tmlr.

We thank you for your essential contribution to TMLR!

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        ## Update the official recommendation and don't send the email again
        official_recommendation_note = javier_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Official_Recommendation',
            signatures=[javier_anon_groups[0].id],
            note=Note(
                id=official_recommendation_note['note']['id'],
                content={
                    'decision_recommendation': { 'value': 'Leaning Accept' },
                    'certification_recommendations': { 'value': ['Survey Certification'] },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Evaluate reviewers and submit decision for TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 1

        ## Check permissions of the review revisions
        review_revisions=openreview_client.get_note_edits(note_id=reviews[0].id)
        assert len(review_revisions) == 3
        assert review_revisions[0].readers == [venue_id, f"{venue_id}/Paper1/Action_Editors", david_anon_groups[0].id]
        assert review_revisions[0].invitation == f"{venue_id}/Paper1/-/Review"
        assert review_revisions[1].readers == [venue_id, f"{venue_id}/Paper1/Action_Editors", david_anon_groups[0].id]
        assert review_revisions[1].invitation == f"{venue_id}/Paper1/-/Review_Release"
        assert review_revisions[2].readers == [venue_id, f"{venue_id}/Paper1/Action_Editors", david_anon_groups[0].id]
        assert review_revisions[2].invitation == f"{venue_id}/Paper1/-/Review"

        review_revisions=openreview_client.get_note_edits(note_id=reviews[1].id)
        assert len(review_revisions) == 2
        assert review_revisions[0].readers == [venue_id, f"{venue_id}/Paper1/Action_Editors", javier_anon_groups[0].id]
        assert review_revisions[0].invitation == f"{venue_id}/Paper1/-/Review_Release"
        assert review_revisions[1].readers == [venue_id, f"{venue_id}/Paper1/Action_Editors", javier_anon_groups[0].id]
        assert review_revisions[1].invitation == f"{venue_id}/Paper1/-/Review"

        review_revisions=openreview_client.get_note_edits(note_id=reviews[2].id)
        assert len(review_revisions) == 2
        assert review_revisions[0].readers == [venue_id, f"{venue_id}/Paper1/Action_Editors", carlos_anon_groups[0].id]
        assert review_revisions[0].invitation == f"{venue_id}/Paper1/-/Review_Release"
        assert review_revisions[1].readers == [venue_id, f"{venue_id}/Paper1/Action_Editors", carlos_anon_groups[0].id]
        assert review_revisions[1].invitation == f"{venue_id}/Paper1/-/Review"

        reviews=openreview_client.get_notes(forum=note_id_1, invitation=f'{venue_id}/Paper1/-/Review', sort= 'number:asc')
        for review in reviews:
            signature=review.signatures[0]

            openreview_client.post_invitation_edit(
                invitations='TMLR/-/Edit',
                signatures=['TMLR'],
                invitation=openreview.api.Invitation(
                    id=f'{signature}/-/Rating',
                    cdate=openreview.tools.datetime_millis(datetime.datetime.now()-datetime.timedelta(days=1)),
                    duedate=openreview.tools.datetime_millis(datetime.datetime.now()-datetime.timedelta(minutes=30)) #set duedate in the past
                )
            )

            rating_note=joelle_client.post_note_edit(invitation=f'{signature}/-/Rating',
                signatures=[joelle_paper1_anon_group.id],
                note=Note(
                    content={
                        'rating': { 'value': 'Exceeds expectations' }
                    }
                )
            )
            helpers.await_queue_edit(openreview_client, edit_id=rating_note['id'])
            process_logs = openreview_client.get_process_logs(id = rating_note['id'])
            assert len(process_logs) == 1
            assert process_logs[0]['status'] == 'ok'

        ## edit last rating
        joelle_client.post_note_edit(invitation=rating_note['invitation'],
            signatures=[joelle_paper1_anon_group.id],
            note=Note(
                id = rating_note['note']['id'],
                content={
                    'rating': { 'value': 'Falls below expectations' }
                }
            )
        )

        last_rating_invitation = openreview_client.get_invitation(rating_note['invitation'])

        invitation = raia_client.get_invitation(f'{venue_id}/Paper1/-/Decision')
        assert invitation.edit['note']['content']['certifications']['value']['param']['enum'] == ['Featured Certification', 'Reproducibility Certification', 'Survey Certification']
        assert invitation.cdate == last_rating_invitation.cdate
        assert invitation.duedate == last_rating_invitation.duedate
        assert not invitation.expdate

        with pytest.raises(openreview.OpenReviewException, match=r'Decision should not be "Accept as is" if you answered "No" to either of the two TMLR criteria'):
            decision_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Decision',
                signatures=[joelle_paper1_anon_group.id],
                note=Note(
                    content={
                        'claims_and_evidence': { 'value': 'No' },
                        'claims_explanation': { 'value': 'Accept as is' },
                        'audience': { 'value': 'Yes' },
                        'audience_explanation': { 'value': 'Accept as is' },
                        'recommendation': { 'value': 'Accept as is' },
                        'certifications': { 'value': ['Featured Certification', 'Reproducibility Certification'] },
                        'additional_comments': { 'value': 'This is a nice paper!' },
                        'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                        'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                    }
                )
            )

        with pytest.raises(openreview.OpenReviewException, match=r'Decision should be "Accept as is" or "Accept with minor revision" if you answered "Yes" to both TMLR criteria'):
            decision_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Decision',
                signatures=[joelle_paper1_anon_group.id],
                note=Note(
                    content={
                        'claims_and_evidence': { 'value': 'Yes' },
                        'claims_explanation': { 'value': 'Reject' },
                        'audience': { 'value': 'Yes' },
                        'audience_explanation': { 'value': 'Reject' },
                        'recommendation': { 'value': 'Reject' },
                        'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                        'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                    }
                )
            )

        # post 'Accept as is' decision
        decision_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Decision',
                signatures=[joelle_paper1_anon_group.id],
                note=Note(
                    content={
                        'claims_and_evidence': { 'value': 'Yes' },
                        'claims_explanation': { 'value': 'Accept as is' },
                        'audience': { 'value': 'Yes' },
                        'audience_explanation': { 'value': 'Accept as is' },
                        'recommendation': { 'value': 'Accept as is' },
                        'certifications': { 'value': ['Featured Certification', 'Reproducibility Certification'] },
                        'additional_comments': { 'value': 'Great paper!' },
                        'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                        'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                    }
                )
            )

        helpers.await_queue_edit(openreview_client, edit_id=decision_note['id'])

        decision_note = joelle_client.get_note(decision_note['note']['id'])
        assert decision_note.readers == [f"{venue_id}/Editors_In_Chief", f"{venue_id}/Paper1/Action_Editors"]
        assert decision_note.writers == [venue_id, f"{venue_id}/Paper1/Action_Editors"]

        submission = openreview_client.get_note(note_id_1)
        assert 'TMLR/Decision_Pending' == submission.content['venueid']['value']

        ## Second decision note and get an error
        with pytest.raises(openreview.OpenReviewException, match=r'You have reached the maximum number \(1\) of replies for this Invitation'):
            decision_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Decision',
                signatures=[joelle_paper1_anon_group.id],
                note=Note(
                    content={
                        'claims_and_evidence': { 'value': 'Yes' },
                        'claims_explanation': { 'value': 'Accept as is' },
                        'audience': { 'value': 'Yes' },
                        'audience_explanation': { 'value': 'Accept as is' },
                        'recommendation': { 'value': 'Accept as is' },
                        'certifications': { 'value': ['Featured Certification', 'Reproducibility Certification'] },
                        'additional_comments': { 'value': 'Great paper!' },
                        'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                        'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                    }
                )
            )

        ## Check invitations
        invitations = raia_client.get_invitations(replyForum=note_id_1)
        assert f"{venue_id}/Paper1/-/Decision_Approval"  in [i.id for i in invitations]

        ## EIC approves the decision
        approval_note = raia_client.post_note_edit(invitation='TMLR/Paper1/-/Decision_Approval',
                            signatures=['TMLR/Editors_In_Chief'],
                            note=Note(
                                content= {
                                    'approval': { 'value': 'I approve the AE\'s decision.' },
                                    'comment_to_the_AE': { 'value': 'I agree with the AE' }
                                }
                            ))

        helpers.await_queue_edit(openreview_client, edit_id=approval_note['id'])

        assert openreview_client.get_invitation(f"{venue_id}/Paper1/-/Review").expdate < openreview.tools.datetime_millis(datetime.datetime.now())
        assert openreview_client.get_invitation(f"{venue_id}/Paper1/-/Official_Recommendation").expdate < openreview.tools.datetime_millis(datetime.datetime.now())

        decision_note = raia_client.get_note(decision_note.id)
        assert decision_note.readers == ['everyone']
        assert decision_note.writers == ['TMLR']
        assert decision_note.nonreaders == []

        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Decision approved for submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Joelle Pineau,
        
Your decision on submission 1: Paper title UPDATED has been approved by the Editors in Chief. The decision is now public.

To know more about the decision, please follow this link: https://openreview.net/forum?id={note_id_1}


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''        

        messages = journal.client.get_messages(to = 'test@mail.com', subject = '[TMLR] Decision for your TMLR submission 1: Paper title UPDATED')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi SomeFirstName User,

We are happy to inform you that, based on the evaluation of the reviewers and the recommendation of the assigned Action Editor, your TMLR submission "1: Paper title UPDATED" is accepted as is.

To know more about the decision and submit the deanonymized camera ready version of your manuscript, please follow this link and click on button "Camera Ready Revision": https://openreview.net/forum?id={note_id_1}. Please submit the final version of your paper within 4 weeks ({(datetime.datetime.now() + datetime.timedelta(weeks = 4)).strftime("%b %d")}).

In addition to your final manuscript, we strongly encourage you to submit a link to 1) code associated with your and 2) a short video presentation of your work. You can provide these links to the corresponding entries on the revision page.

For more details and guidelines on the TMLR review process, visit jmlr.org/tmlr.

We thank you for your contribution to TMLR and congratulate you for your successful submission!

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        assert openreview_client.get_invitation(f"{venue_id}/Paper1/-/Camera_Ready_Revision")
        
        ## check camera ready reminder
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/-/Camera_Ready_Revision',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 10)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 1)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/-/Camera_Ready_Revision-0-0')        
        
        messages = journal.client.get_messages(to = 'test@mail.com', subject = '[TMLR] You are late in performing a task for your paper 1: Paper title UPDATED')
        assert len(messages) == 1
        
        
        ## post a revision
        revision_note = test_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/Camera_Ready_Revision',
            signatures=[f"{venue_id}/Paper1/Authors"],
            note=Note(
                content={
                    'title': { 'value': 'Paper title VERSION 2' },
                    'authors': { 'value': ['Melissa Eight', 'SomeFirstName User', 'Andrew McCallum'] },
                    'authorids': { 'value': ['~Melissa_Eight1', '~SomeFirstName_User1', '~Andrew_McCallumm1'] },
                    'abstract': { 'value': 'Paper abstract' },
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'video': { 'value': 'https://youtube.com/dfenxkw'}
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=revision_note['id'])

        ## check camera ready reminder
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/-/Camera_Ready_Revision',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 10)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 7)) + 2000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/-/Camera_Ready_Revision-0-1')        
        
        messages = journal.client.get_messages(to = 'test@mail.com', subject = '[TMLR] You are late in performing a task for your paper 1: Paper title UPDATED')
        assert len(messages) == 1        

        note = openreview_client.get_note(note_id_1)
        assert note
        assert note.forum == note_id_1
        assert note.replyto is None
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/Paper1/-/Revision', 'TMLR/-/Edit', 'TMLR/-/Under_Review', 'TMLR/Paper1/-/Camera_Ready_Revision']
        assert note.readers == ['everyone']
        assert note.writers == ['TMLR', 'TMLR/Paper1/Authors']
        assert note.signatures == ['TMLR/Paper1/Authors']
        assert note.content['authorids']['value'] == ['~Melissa_Eight1', '~SomeFirstName_User1', '~Andrew_McCallumm1']
        assert note.content['authors']['value'] == ['Melissa Eight', 'SomeFirstName User', 'Andrew McCallum']
        assert note.content['venue']['value'] == 'Decision pending for TMLR'
        assert note.content['venueid']['value'] == 'TMLR/Decision_Pending'
        assert note.content['title']['value'] == 'Paper title VERSION 2'
        assert note.content['abstract']['value'] == 'Paper abstract'

        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Review camera ready version for TMLR paper 1: Paper title VERSION 2')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Joelle Pineau,

The authors of TMLR paper 1: Paper title VERSION 2 have now submitted the deanonymized camera ready version of their work.

As your final task for this submission, please verify that the camera ready manuscript complies with the TMLR stylefile, with all author information inserted in the manuscript as well as the link to the OpenReview page for the submission.

Moreover, if the paper was accepted with minor revision, verify that the changes requested have been followed.

Visit the following link to perform this task: https://openreview.net/forum?id={note_id_1}&invitationId=TMLR/Paper1/-/Camera_Ready_Verification

If any correction is needed, you may contact the authors directly by email or through OpenReview.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        ## Check reminders
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/-/Camera_Ready_Verification',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 10)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 7)) + 2000
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/-/Camera_Ready_Verification-0-1')

        messages = journal.client.get_messages(subject = '[TMLR] You are late in performing a task for assigned paper 1: Paper title VERSION 2')
        assert len(messages) == 1

        messages = journal.client.get_messages(subject = '[TMLR] AE is late in performing a task for assigned paper 1: Paper title VERSION 2')
        assert len(messages) == 2

        messages = journal.client.get_messages(to='raia@mail.com', subject = '[TMLR] AE is late in performing a task for assigned paper 1: Paper title VERSION 2')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Raia Hadsell,

Our records show that the AE for submission 1: Paper title VERSION 2 is *one week* late on an AE task:

Task: Camera Ready Verification
AE: Joelle Pineau
Link: https://openreview.net/forum?id={note_id_1}

OpenReview Team


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        ## Check reminders
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper1/-/Camera_Ready_Verification',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 40)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 30)) + 2000
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper1/-/Camera_Ready_Verification-0-2')

        messages = journal.client.get_messages(subject = '[TMLR] You are late in performing a task for assigned paper 1: Paper title VERSION 2')
        assert len(messages) == 1

        messages = journal.client.get_messages(subject = '[TMLR] AE is late in performing a task for assigned paper 1: Paper title VERSION 2')
        assert len(messages) == 4

        messages = journal.client.get_messages(to='raia@mail.com', subject = '[TMLR] AE is late in performing a task for assigned paper 1: Paper title VERSION 2')
        assert len(messages) == 2

        ## AE verifies the camera ready revision
        verification_note = joelle_client.post_note_edit(invitation='TMLR/Paper1/-/Camera_Ready_Verification',
                            signatures=[joelle_paper1_anon_group.id],
                            note=Note(
                                signatures=[joelle_paper1_anon_group.id],
                                content= {
                                    'verification': { 'value': 'I confirm that camera ready manuscript complies with the TMLR stylefile and, if appropriate, includes the minor revisions that were requested.' }
                                 }
                            ))

        helpers.await_queue_edit(openreview_client, edit_id=verification_note['id'])

        ## check late invitees again
        assert journal.get_late_invitees('TMLR/Paper1/-/Camera_Ready_Verification') == []

        messages = journal.client.get_messages(to = 'test@mail.com', subject = '[TMLR] Camera ready version accepted for your TMLR submission 1: Paper title VERSION 2')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi SomeFirstName User,

This is to inform you that your submitted camera ready version of your paper 1: Paper title VERSION 2 has been verified and confirmed by the Action Editor.

We thank you again for your contribution to TMLR and congratulate you for your successful submission!

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        note = openreview_client.get_note(note_id_1)
        assert note
        assert note.forum == note_id_1
        assert note.replyto is None
        assert note.pdate
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/Paper1/-/Revision', 'TMLR/-/Edit', 'TMLR/-/Under_Review', 'TMLR/Paper1/-/Camera_Ready_Revision', 'TMLR/-/Accepted']
        assert note.readers == ['everyone']
        assert note.writers == ['TMLR']
        assert note.signatures == ['TMLR/Paper1/Authors']
        assert note.content['authorids']['value'] == ['~Melissa_Eight1', '~SomeFirstName_User1', '~Andrew_McCallumm1']
        assert note.content['authors']['value'] == ['Melissa Eight', 'SomeFirstName User', 'Andrew McCallum']
        # Check with cArlos
        assert note.content['authorids'].get('readers') is None
        assert note.content['authors'].get('readers') is None
        assert note.content['supplementary_material'].get('readers') is None
        assert note.content['venue']['value'] == 'Accepted by TMLR'
        assert note.content['venueid']['value'] == 'TMLR'
        assert note.content['title']['value'] == 'Paper title VERSION 2'
        assert note.content['abstract']['value'] == 'Paper abstract'
        assert note.content['certifications']['value'] == ['Featured Certification', 'Reproducibility Certification', 'Expert Certification']
        assert note.content['expert_reviewers']['value'] == ['~Andrew_McCallumm1']
        assert note.content['_bibtex']['value'] == '''@article{
eight''' + str(datetime.datetime.fromtimestamp(note.cdate/1000).year) + '''paper,
title={Paper title {VERSION} 2},
author={Melissa Eight and SomeFirstName User and Andrew McCallum},
journal={Transactions on Machine Learning Research},
issn={2835-8856},
year={''' + str(datetime.datetime.today().year) + '''},
url={https://openreview.net/forum?id=''' + note_id_1 + '''},
note={Featured Certification, Reproducibility Certification, Expert Certification}
}'''

        helpers.await_queue_edit(openreview_client, invitation='TMLR/-/Accepted')

        ## Check invitations are expired
        invitations = openreview_client.get_invitations(prefix=f"{venue_id}/Paper1/.*", type = "all")
        assert len(invitations) == 5
        assert f"{venue_id}/Paper1/-/Official_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Public_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Moderation" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/Retraction" in [i.id for i in invitations]
        assert f"{venue_id}/Paper1/-/EIC_Revision" in [i.id for i in invitations]

        ## Update the paper by the EICs
        revision_note = raia_client.post_note_edit(invitation=f'{venue_id}/Paper1/-/EIC_Revision',
            signatures=[f"{venue_id}/Editors_In_Chief"],
            note=Note(
                content={
                    'title': { 'value': 'Paper title VERSION 2' },
                    'authors': { 'value': ['Melissa Eight', 'SomeFirstName User', 'Celeste Ana Martinez', 'Andrew McCallum'] },
                    'authorids': { 'value': ['~Melissa_Eight1', '~SomeFirstName_User1', '~Celeste_Ana_Martinez1', '~Andrew_McCallumm1'] },
                    'abstract': { 'value': 'Paper abstract' },
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'video': { 'value': 'https://youtube.com/dfenxkw'},
                    'certifications': { 'value': ['Featured Certification', 'Reproducibility Certification', 'Expert Certification', 'Outstanding Certification'] },
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=revision_note['id'])

        note = openreview_client.get_note(note_id_1)
        assert note
        assert note.forum == note_id_1
        assert note.replyto is None
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/Paper1/-/Revision', 'TMLR/-/Edit', 'TMLR/-/Under_Review', 'TMLR/Paper1/-/Camera_Ready_Revision', 'TMLR/-/Accepted', 'TMLR/Paper1/-/EIC_Revision']
        assert note.readers == ['everyone']
        assert note.writers == ['TMLR']
        assert note.signatures == ['TMLR/Paper1/Authors']
        assert note.content['authorids']['value'] == ['~Melissa_Eight1', '~SomeFirstName_User1', '~Celeste_Ana_Martinez1', '~Andrew_McCallumm1']
        assert note.content['authors']['value'] == ['Melissa Eight', 'SomeFirstName User', 'Celeste Ana Martinez', 'Andrew McCallum']
        # Check with cArlos
        assert note.content['authorids'].get('readers') is None
        assert note.content['authors'].get('readers') is None
        assert note.content['supplementary_material'].get('readers') is None
        assert note.content['venue']['value'] == 'Accepted by TMLR'
        assert note.content['venueid']['value'] == 'TMLR'
        assert note.content['title']['value'] == 'Paper title VERSION 2'
        assert note.content['abstract']['value'] == 'Paper abstract'
        assert note.content['_bibtex']['value'] == '''@article{
eight''' + str(datetime.datetime.fromtimestamp(note.cdate/1000).year) + '''paper,
title={Paper title {VERSION} 2},
author={Melissa Eight and SomeFirstName User and Celeste Ana Martinez and Andrew McCallum},
journal={Transactions on Machine Learning Research},
issn={2835-8856},
year={''' + str(datetime.datetime.today().year) + '''},
url={https://openreview.net/forum?id=''' + note_id_1 + '''},
note={Featured Certification, Reproducibility Certification, Expert Certification, Outstanding Certification}
}'''

        ## Retract the paper
        retraction_note = test_client.post_note_edit(invitation='TMLR/Paper1/-/Retraction',
                            signatures=[f"{venue_id}/Paper1/Authors"],
                            note=Note(
                                signatures=[f"{venue_id}/Paper1/Authors"],
                                content= {
                                    'retraction_confirmation': { 'value': 'I have read and agree with the venue\'s retraction policy on behalf of myself and my co-authors.' }
                                 }
                            ))

        helpers.await_queue_edit(openreview_client, edit_id=retraction_note['id'])

        messages = journal.client.get_messages(subject = '[TMLR] Authors request to retract TMLR submission 1: Paper title VERSION 2')
        assert len(messages) == 2
        messages = journal.client.get_messages(to='raia@mail.com', subject = '[TMLR] Authors request to retract TMLR submission 1: Paper title VERSION 2')
        assert messages[0]['content']['text'] == f'''Hi Raia Hadsell,

The authors of paper 1: Paper title VERSION 2 are requesting to retract the paper. An EIC must confirm and accept the retraction: https://openreview.net/forum?id={note_id_1}&invitationId=TMLR/Paper1/-/Retraction_Approval

OpenReview Team


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''
        assert openreview_client.get_invitation(f"{venue_id}/Paper1/-/Retraction_Approval")

        approval_note = raia_client.post_note_edit(invitation='TMLR/Paper1/-/Retraction_Approval',
                            signatures=[f"{venue_id}/Editors_In_Chief"],
                            note=Note(
                                signatures=[f"{venue_id}/Editors_In_Chief"],
                                content= {
                                    'approval': { 'value': 'Yes' }
                                 }
                            ))

        helpers.await_queue_edit(openreview_client, edit_id=approval_note['id'])

        messages = journal.client.get_messages(subject = '[TMLR] Decision available for retraction request of TMLR submission 1: Paper title VERSION 2')
        assert len(messages) == 4
        messages = journal.client.get_messages(to='test@mail.com', subject = '[TMLR] Decision available for retraction request of TMLR submission 1: Paper title VERSION 2')
        assert messages[0]['content']['text'] == f'''Hi SomeFirstName User,

As TMLR Editors-in-Chief, we have submitted our decision on your request to retract your accepted paper at TMLR "1: Paper title VERSION 2".

To view our decision, follow this link: https://openreview.net/forum?id={note_id_1}&noteId={approval_note['note']['id']}

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        note = openreview_client.get_note(retraction_note['note']['id'])
        assert note.readers == ['everyone']
        assert note.nonreaders == []

        note = openreview_client.get_note(note_id_1)
        assert note
        assert note.forum == note_id_1
        assert note.replyto is None
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/Paper1/-/Revision', 'TMLR/-/Edit', 'TMLR/-/Under_Review', 'TMLR/Paper1/-/Camera_Ready_Revision', 'TMLR/-/Accepted', 'TMLR/Paper1/-/EIC_Revision', 'TMLR/-/Retracted']
        assert note.readers == ['everyone']
        assert note.writers == ['TMLR']
        assert note.signatures == ['TMLR/Paper1/Authors']
        assert note.content['authorids']['value'] == ['~Melissa_Eight1', '~SomeFirstName_User1', '~Celeste_Ana_Martinez1', '~Andrew_McCallumm1']
        # Check with cArlos
        assert note.content['authorids'].get('readers') is None
        assert note.content['authors'].get('readers') is None
        assert note.content['supplementary_material'].get('readers') is None
        assert note.content['venue']['value'] == 'Retracted by Authors'
        assert note.content['venueid']['value'] == 'TMLR/Retracted_Acceptance'
        assert note.content['title']['value'] == 'Paper title VERSION 2'
        assert note.content['abstract']['value'] == 'Paper abstract'
        assert note.content['_bibtex']['value'] == '''@article{
eight''' + str(datetime.datetime.fromtimestamp(note.cdate/1000).year) + '''paper,
title={Paper title {VERSION} 2},
author={Melissa Eight and SomeFirstName User and Celeste Ana Martinez and Andrew McCallum},
journal={Submitted to Transactions on Machine Learning Research},
year={''' + str(datetime.datetime.today().year) + '''},
url={https://openreview.net/forum?id=''' + note_id_1 + '''},
note={Retracted after acceptance}
}'''


        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'], process_index=0)
        helpers.await_queue_edit(openreview_client, edit_id=hugo_review_note['id'], process_index=0)
        helpers.await_queue_edit(openreview_client, edit_id=antony_review_note['id'], process_index=0)
        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'], process_index=0)
        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'], process_index=0)

        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'], process_index=1)
        helpers.await_queue_edit(openreview_client, edit_id=hugo_review_note['id'], process_index=1)
        helpers.await_queue_edit(openreview_client, edit_id=antony_review_note['id'], process_index=1)
        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'], process_index=1)
        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'], process_index=1)

    def test_rejected_submission(self, journal, openreview_client, test_client, helpers):

        venue_id = journal.venue_id
        editor_in_chief_group_id = journal.get_editors_in_chief_id()
        test_client = OpenReviewClient(username='test@mail.com', password=helpers.strong_password)
        raia_client = OpenReviewClient(username='raia@mail.com', password=helpers.strong_password)
        joelle_client = OpenReviewClient(username='joelle@mailseven.com', password=helpers.strong_password)
        peter_client = OpenReviewClient(username='petersnow@yahoo.com', password=helpers.strong_password)
        tom_client=helpers.create_user('tom@mail.com', 'Tom', 'Rain')



        ## Reviewers
        david_client=OpenReviewClient(username='david@mailone.com', password=helpers.strong_password)
        javier_client=OpenReviewClient(username='javier@mailtwo.com', password=helpers.strong_password)
        carlos_client=OpenReviewClient(username='carlos@mailthree.com', password=helpers.strong_password)
        andrew_client=OpenReviewClient(username='andrewmc@mailfour.com', password=helpers.strong_password)
        hugo_client=OpenReviewClient(username='hugo@mailsix.com', password=helpers.strong_password)

        now = datetime.datetime.now()

        ## Post the submission 4
        submission_note_4 = test_client.post_note_edit(invitation='TMLR/-/Submission',
            signatures=['~SomeFirstName_User1'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 4' },
                    'abstract': { 'value': 'Paper abstract' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1']},
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'submission_length': { 'value': 'Long submission (more than 12 pages of main content)'}
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_4['id'])
        note_id_4=submission_note_4['note']['id']

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        openreview_client.get_invitation('TMLR/Paper4/Action_Editors/-/Recommendation')        

        # Assign Action Editor
        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_4,
            tail='~Joelle_Pineau1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ## Accept the submission 4 as an EIC
        under_review_note = raia_client.post_note_edit(invitation= 'TMLR/Paper4/-/Review_Approval',
                                    signatures=[f'{venue_id}/Editors_In_Chief'],
                                    note=Note(content={
                                        'under_review': { 'value': 'Appropriate for Review' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=under_review_note['id'])

        edits = openreview_client.get_note_edits(note_id=note_id_4, invitation='TMLR/-/Under_Review')

        helpers.await_queue_edit(openreview_client, edit_id=edits[0].id)

        joelle_paper4_anon_groups = joelle_client.get_groups(prefix=f'{venue_id}/Paper4/Action_Editor_.*', signatory='~Joelle_Pineau1')
        assert len(joelle_paper4_anon_groups) == 1
        joelle_paper4_anon_group = joelle_paper4_anon_groups[0]         

        ## Assign David Belanger
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper4/Action_Editors", '~David_Belanger1'],
            nonreaders=[f"{venue_id}/Paper4/Authors"],
            writers=[venue_id, f"{venue_id}/Paper4/Action_Editors"],
            signatures=[joelle_paper4_anon_group.id],
            head=note_id_4,
            tail='~David_Belanger1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        messages = journal.client.get_messages(to = 'david@mailone.com', subject = '[TMLR] Assignment to review new TMLR submission 4: Paper title 4')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi David Belanger,

With this email, we request that you submit, within 4 weeks ({(datetime.datetime.now() + datetime.timedelta(weeks = 4)).strftime("%b %d")}) a review for your newly assigned TMLR submission "4: Paper title 4". If the submission is longer than 12 pages (excluding any appendix), you may request more time to the AE.

Please acknowledge on OpenReview that you have received this review assignment by following this link: https://openreview.net/forum?id={note_id_4}&invitationId=TMLR/Paper4/Reviewers/-/~David_Belanger1/Assignment/Acknowledgement

As a reminder, reviewers are **expected to accept all assignments** for submissions that fall within their expertise and annual quota (6 papers). Acceptable exceptions are 1) if you have an active, unsubmitted review for another TMLR submission or 2) situations where exceptional personal circumstances (e.g. vacation, health problems) render you incapable of performing your reviewing duties. Based on the above, if you think you should not review this submission, contact your AE directly (you can do so by leaving a comment on OpenReview, with only the Action Editor as Reader).

To submit your review, please follow this link: https://openreview.net/forum?id={note_id_4}&invitationId=TMLR/Paper4/-/Review or check your tasks in the Reviewers Console: https://openreview.net/group?id=TMLR/Reviewers#reviewer-tasks

Once submitted, your review will become privately visible to the authors and AE. Then, as soon as 3 reviews have been submitted, all reviews will become publicly visible. For more details and guidelines on performing your review, visit jmlr.org/tmlr.

We thank you for your essential contribution to TMLR!

The TMLR Editors-in-Chief
note: replies to this email will go to the AE, Joelle Pineau.


Please note that responding to this email will direct your reply to joelle@mailseven.com.
'''

        ## Assign Carlos Mondragon
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper4/Action_Editors", '~Carlos_Mondragon1'],
            nonreaders=[f"{venue_id}/Paper4/Authors"],
            writers=[venue_id, f"{venue_id}/Paper4/Action_Editors"],
            signatures=[joelle_paper4_anon_group.id],
            head=note_id_4,
            tail='~Carlos_Mondragon1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ## Assign Javier Burroni
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper4/Action_Editors", '~Javier_Burroni1'],
            nonreaders=[f"{venue_id}/Paper4/Authors"],
            writers=[venue_id, f"{venue_id}/Paper4/Action_Editors"],
            signatures=[joelle_paper4_anon_group.id],
            head=note_id_4,
            tail='~Javier_Burroni1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ## Check pending review edges
        edges = joelle_client.get_grouped_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', groupby='weight')
        assert len(edges) == 2

        if len(edges[0]['values']) == 3:
            assert edges[0]['id']['weight'] == 1
            assert edges[1]['id']['weight'] == 0
            assert len(edges[1]['values']) == 2
        else:
            assert edges[0]['id']['weight'] == 0
            assert len(edges[0]['values']) == 2
            assert edges[1]['id']['weight'] == 1
            assert len(edges[1]['values']) == 3

        if len(edges[0]['values']) == 2:
            assert edges[0]['id']['weight'] == 0
            assert edges[1]['id']['weight'] == 1
            assert len(edges[1]['values']) == 3
        else:
            assert edges[0]['id']['weight'] == 1
            assert len(edges[0]['values']) == 3
            assert edges[1]['id']['weight'] == 0
            assert len(edges[1]['values']) == 2

        ## Ask solicit review and then delete it
        celeste_client = OpenReviewClient(username='celeste@mailnine.com', password=helpers.strong_password)

        volunteer_to_review_note = celeste_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/Volunteer_to_Review',
            signatures=['~Celeste_Ana_Martinez1'],
            note=Note(
                content={
                    'solicit': { 'value': 'I solicit to review this paper.' },
                    'comment': { 'value': 'I can review this paper.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=volunteer_to_review_note['id'])

        assert openreview_client.get_invitation(f'{venue_id}/Paper4/-/~Celeste_Ana_Martinez1_Volunteer_to_Review_Approval')
        assert openreview_client.get_invitation(f'{venue_id}/Paper4/Volunteer_to_Review1/-/Volunteer_to_Review_Comment')

        volunteer_to_review_note = celeste_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/Volunteer_to_Review',
            signatures=['~Celeste_Ana_Martinez1'],
            note=Note(
                id=volunteer_to_review_note['note']['id'],
                ddate=openreview.tools.datetime_millis(datetime.datetime.now()),
                content={
                    'solicit': { 'value': 'I solicit to review this paper.' },
                    'comment': { 'value': 'I can review this paper.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=volunteer_to_review_note['id'])

        ## approval must be expired
        invitation = openreview_client.get_invitation(f'{venue_id}/Paper4/-/~Celeste_Ana_Martinez1_Volunteer_to_Review_Approval') 
        assert invitation.is_active() == False

        ## volunteer comment must be expired
        invitation = openreview_client.get_invitation(f'{venue_id}/Paper4/Volunteer_to_Review1/-/Volunteer_to_Review_Comment')
        assert invitation.is_active() == False

        ## Ask solicit review with a conflict
        volunteer_to_review_note = tom_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/Volunteer_to_Review',
            signatures=['~Tom_Rain1'],
            note=Note(
                content={
                    'solicit': { 'value': 'I solicit to review this paper.' },
                    'comment': { 'value': 'I can review this paper.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=volunteer_to_review_note['id'])

        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Request to review TMLR submission "4: Paper title 4" has been submitted')
        assert len(messages) == 2
        assert messages[-1]['content']['text'] == f'''Hi Joelle Pineau,

This is to inform you that an OpenReview user (Tom Rain) has requested to review TMLR submission 4: Paper title 4, which you are the AE for.

Please consult the request and either accept or reject it, by visiting this link:

https://openreview.net/forum?id={note_id_4}&noteId={volunteer_to_review_note['note']['id']}

We ask that you provide a response within 1 week, by {(datetime.datetime.now() + datetime.timedelta(weeks = 1)).strftime("%b %d")}. Note that it is your responsibility to ensure that this submission is assigned to qualified reviewers and is evaluated fairly. Therefore, make sure to overview the user’s profile (https://openreview.net/profile?id=~Tom_Rain1) before making a decision.

We thank you for your contribution to TMLR!

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        ## Post a response
        with pytest.raises(openreview.OpenReviewException, match=r'Can not approve this solicit review: conflict detected for ~Tom_Rain1'):
            Volunteer_to_Review_approval_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/~Tom_Rain1_Volunteer_to_Review_Approval',
                signatures=[joelle_paper4_anon_group.id],
                note=Note(
                    content={
                        'decision': { 'value': 'Yes, I approve the solicit review.' },
                        'comment': { 'value': 'thanks!' }
                    }
                )
            )

        ## Ask solicit review
        Volunteer_to_Review_note = peter_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/Volunteer_to_Review',
            signatures=['~Peter_Snow1'],
            note=Note(
                content={
                    'solicit': { 'value': 'I solicit to review this paper.' },
                    'comment': { 'value': 'I can review this paper.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=Volunteer_to_Review_note['id'])

        invitations = joelle_client.get_invitations(replyForum=note_id_4)
        assert f'{venue_id}/Paper4/-/~Peter_Snow1_Volunteer_to_Review_Approval' in [i.id for i in invitations]

        # assert AE can commmunicate with volunteer before approval
        comment = peter_client.post_note_edit(invitation=f'{venue_id}/Paper4/Volunteer_to_Review3/-/Volunteer_to_Review_Comment',
            signatures=['~Peter_Snow1'],
            note=Note(
                content={
                    'comment': { 'value': 'I would really like to review this submission' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=comment['id'])

        comment = openreview_client.get_note(comment['note']['id'])
        assert comment.readers == [ 'TMLR/Editors_In_Chief', 'TMLR/Paper4/Action_Editors', '~Peter_Snow1' ]

        messages = journal.client.get_messages(to = 'petersnow@yahoo.com', subject = '[TMLR] Comment posted on submission 4: "Paper title 4" pertaining to volunteer reviewing')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Your comment pertaining to volunteer reviewing on a submission has been posted.

Submission: Paper title 4

Comment: I would really like to review this submission

To view the comment, click here: https://openreview.net/forum?id={note_id_4}&noteId={comment.id}'''

        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Comment posted on submission 4: "Paper title 4" pertaining to volunteer reviewing')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''A comment pertaining to volunteer reviewing on a submission has been posted.

Submission: Paper title 4

Comment: I would really like to review this submission

To view the comment, click here: https://openreview.net/forum?id={note_id_4}&noteId={comment.id}'''

        comment = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper4/Volunteer_to_Review3/-/Volunteer_to_Review_Comment',
            signatures=[joelle_paper4_anon_group.id],
            note=Note(
                content={
                    'comment': { 'value': 'I am still considering other reviewers.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=comment['id'])

        comment = openreview_client.get_note(comment['note']['id'])
        assert comment.readers == [ 'TMLR/Editors_In_Chief', 'TMLR/Paper4/Action_Editors', '~Peter_Snow1' ]

        messages = journal.client.get_messages(to = 'petersnow@yahoo.com', subject = '[TMLR] Comment posted on submission 4: "Paper title 4" pertaining to volunteer reviewing')
        assert len(messages) == 2
        assert messages[-1]['content']['text'] == f'''A comment pertaining to volunteer reviewing on a submission has been posted.

Submission: Paper title 4

Comment: I am still considering other reviewers.

To view the comment, click here: https://openreview.net/forum?id={note_id_4}&noteId={comment.id}'''

        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Comment posted on submission 4: "Paper title 4" pertaining to volunteer reviewing')
        assert len(messages) == 2
        assert messages[-1]['content']['text'] == f'''Your comment pertaining to volunteer reviewing on a submission has been posted.

Submission: Paper title 4

Comment: I am still considering other reviewers.

To view the comment, click here: https://openreview.net/forum?id={note_id_4}&noteId={comment.id}'''

        ## Post a response
        Volunteer_to_Review_approval_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/~Peter_Snow1_Volunteer_to_Review_Approval',
            signatures=[joelle_paper4_anon_group.id],
            note=Note(
                content={
                    'decision': { 'value': 'Yes, I approve the solicit review.' },
                    'comment': { 'value': 'thanks!' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=Volunteer_to_Review_approval_note['id'])

        assert '~Peter_Snow1' in Volunteer_to_Review_approval_note['note']['readers']

        paper_assignment_edges = openreview_client.get_edges(invitation='TMLR/Reviewers/-/Assignment', tail='~Peter_Snow1', head=note_id_4)
        assert len(paper_assignment_edges) == 1

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edges[0].id)

        assert '~Peter_Snow1' in joelle_client.get_group(f'{venue_id}/Paper4/Reviewers').members

        messages = journal.client.get_messages(to = 'petersnow@yahoo.com', subject = '[TMLR] Request to review TMLR submission "4: Paper title 4" has been accepted')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Peter Snow,

This is to inform you that your request to act as a reviewer for TMLR submission 4: Paper title 4 has been accepted by the Action Editor (AE).

You are required to submit your review within 4 weeks ({(datetime.datetime.now() + datetime.timedelta(weeks = 4)).strftime("%b %d")}). If the submission is longer than 12 pages (excluding any appendix), you may request more time from the AE.

To submit your review, please follow this link: https://openreview.net/forum?id={note_id_4}&invitationId=TMLR/Paper4/-/Review or check your tasks in the Reviewers Console: https://openreview.net/group?id=TMLR/Reviewers

Once submitted, your review will become privately visible to the authors and AE. Then, as soon as 3 reviews have been submitted, all reviews will become publicly visible. For more details and guidelines on performing your review, visit jmlr.org/tmlr.

We thank you for your contribution to TMLR!

The TMLR Editors-in-Chief
note: replies to this email will go to the AE, Joelle Pineau.


Please note that responding to this email will direct your reply to joelle@mailseven.com.
'''

        messages = journal.client.get_messages(to = 'petersnow@yahoo.com', subject = '[TMLR] Assignment to review new TMLR submission 4: Paper title 4')
        assert len(messages) == 0

        assert not journal.client.get_messages(to = 'petersnow@yahoo.com', subject = '[TMLR] Acknowledgement of Reviewer Responsibility')
        assert not openreview.tools.get_invitation(openreview_client, 'TMLR/Reviewers/-/~Peter_Snow1/Responsibility/Acknowledgement')

        ## volunteer comment must be expired
        invitation = openreview_client.get_invitation(f'{venue_id}/Paper4/Volunteer_to_Review3/-/Volunteer_to_Review_Comment')
        assert invitation.is_active() == False

        ## Post a review edit
        david_anon_groups=david_client.get_groups(prefix=f'{venue_id}/Paper4/Reviewer_.*', signatory='~David_Belanger1')
        assert len(david_anon_groups) == 1

        david_review_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/Review',
            signatures=[david_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'])

        messages = journal.client.get_messages(subject = '[TMLR] Review posted on TMLR submission 4: Paper title 4')

        ## Post a review edit
        javier_anon_groups=javier_client.get_groups(prefix=f'{venue_id}/Paper4/Reviewer_.*', signatory='~Javier_Burroni1')
        assert len(javier_anon_groups) == 1
        javier_review_note = javier_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/Review',
            signatures=[javier_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'])

        ## Post a review edit
        carlos_anon_groups=carlos_client.get_groups(prefix=f'{venue_id}/Paper4/Reviewer_.*', signatory='~Carlos_Mondragon1')
        assert len(carlos_anon_groups) == 1
        carlos_review_note = carlos_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/Review',
            signatures=[carlos_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'])

        ## Assign a 4th reviewer
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper4/Action_Editors", '~Hugo_Larochelle1'],
            nonreaders=[f"{venue_id}/Paper4/Authors"],
            writers=[venue_id, f"{venue_id}/Paper4/Action_Editors"],
            signatures=[joelle_paper4_anon_group.id],
            head=note_id_4,
            tail='~Hugo_Larochelle1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        
        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'], process_index=0)
        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'], process_index=0)
        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'], process_index=0)

        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'], process_index=1)
        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'], process_index=1)
        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'], process_index=1)

        ## Check pending review edges
        edges = joelle_client.get_edges_count(invitation='TMLR/Reviewers/-/Pending_Reviews')
        assert edges == 5
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Carlos_Mondragon1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Javier_Burroni1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~David_Belanger1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Hugo_Larochelle1')[0].weight == 1
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Antony_Bal1')[0].weight == 0

        invitation = raia_client.get_invitation(f'{venue_id}/Paper4/-/Official_Recommendation')
        #assert invitation.cdate > openreview.tools.datetime_millis(datetime.datetime.now())

        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper4/-/Official_Recommendation',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now()) + 1000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        time.sleep(5) ## wait until the process function runs
        assert raia_client.get_invitation(f'{venue_id}/Paper4/-/Review_Rating_Enabling')

        ## Post a review recommendation
        official_recommendation_note = carlos_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/Official_Recommendation',
            signatures=[carlos_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Reject' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        ## Post a review recommendation
        official_recommendation_note = javier_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/Official_Recommendation',
            signatures=[javier_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Reject' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        ## Enable review rating before all the recommendations are in
        review_rating_enabling_note = raia_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/Review_Rating_Enabling',
            signatures=['TMLR/Editors_In_Chief'],
            note=Note(
                content={
                    'approval': { 'value': 'I approve enabling review rating even if there are official recommendations missing.' },
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=review_rating_enabling_note['id'])       

        reviews=openreview_client.get_notes(forum=note_id_4, invitation=f'{venue_id}/Paper4/-/Review', sort= 'number:asc')

        for review in reviews:
            signature=review.signatures[0]
            rating_note=joelle_client.post_note_edit(invitation=f'{signature}/-/Rating',
                signatures=[joelle_paper4_anon_group.id],
                note=Note(
                    content={
                        'rating': { 'value': 'Exceeds expectations' }
                    }
                )
            )
            helpers.await_queue_edit(openreview_client, edit_id=rating_note['id'])

        with pytest.raises(openreview.OpenReviewException, match=r'Decision Reject can not have certifications'):
            decision_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/Decision',
                signatures=[joelle_paper4_anon_group.id],
                note=Note(
                    content={
                        'claims_and_evidence': { 'value': 'No' },
                        'claims_explanation': { 'value': 'Accept as is' },
                        'audience': { 'value': 'No' },
                        'audience_explanation': { 'value': 'Accept as is' },
                        'recommendation': { 'value': 'Reject' },
                        'additional_comments': { 'value': 'This is not a good paper' },
                        'certifications': { 'value': ['Featured Certification', 'Reproducibility Certification'] },
                        'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                        'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                    }
                )
            )

        decision_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper4/-/Decision',
            signatures=[joelle_paper4_anon_group.id],
            note=Note(
                content={
                    'claims_and_evidence': { 'value': 'No' },
                    'claims_explanation': { 'value': 'Reject' },
                    'audience': { 'value': 'No' },
                    'audience_explanation': { 'value': 'Reject' },
                    'recommendation': { 'value': 'Reject' },
                    'additional_comments': { 'value': 'This is not a good paper' },
                    'resubmission_of_major_revision': { 'value': 'The authors may consider submitting a major revision at a later time.' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }                   
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=decision_note['id'])

        decision_note = joelle_client.get_note(decision_note['note']['id'])
        assert decision_note.readers == ['TMLR/Editors_In_Chief', f"{venue_id}/Paper4/Action_Editors"]

        ## EIC approves the decision
        approval_note = raia_client.post_note_edit(invitation='TMLR/Paper4/-/Decision_Approval',
                            signatures=['TMLR/Editors_In_Chief'],
                            note=Note(
                            content= {
                                'approval': { 'value': 'I approve the AE\'s decision.' },
                                'comment_to_the_AE': { 'value': 'I agree with the AE' }
                            }))

        helpers.await_queue_edit(openreview_client, edit_id=approval_note['id'])

        decision_note = raia_client.get_note(decision_note.id)
        assert decision_note.readers == ['everyone']

        helpers.await_queue_edit(openreview_client, invitation='TMLR/-/Rejected')

        messages = journal.client.get_messages(to = 'test@mail.com', subject = '[TMLR] Decision for your TMLR submission 4: Paper title 4')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi SomeFirstName User,

We are sorry to inform you that, based on the evaluation of the reviewers and the recommendation of the assigned Action Editor, your TMLR submission "4: Paper title 4" is rejected.

To know more about the decision, please follow this link: https://openreview.net/forum?id={note_id_4}

The action editor might have indicated that they would be willing to consider a significantly revised version of the manuscript. If so, a revised submission will need to be entered as a new submission, that must also provide a link to this previously rejected submission as well as a description of the changes made since.

In any case, your submission will remain publicly available on OpenReview. You may decide to reveal your identity and deanonymize your submission on the OpenReview page. Doing so will however preclude you from submitting any revised version of the manuscript to TMLR.

For more details and guidelines on the TMLR review process, visit jmlr.org/tmlr.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        note = openreview_client.get_note(note_id_4)
        assert note
        assert note.forum == note_id_4
        assert note.replyto is None
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/-/Edit', 'TMLR/-/Under_Review', 'TMLR/-/Rejected']
        assert note.readers == ['everyone']
        assert note.writers == ['TMLR', 'TMLR/Paper4/Authors']
        assert note.signatures == ['TMLR/Paper4/Authors']
        assert note.content['authorids']['value'] == ['~SomeFirstName_User1', '~Melissa_Eight1']
        assert note.content['venue']['value'] == 'Rejected by TMLR'
        assert note.content['venueid']['value'] == 'TMLR/Rejected'
        assert note.content['title']['value'] == 'Paper title 4'
        assert note.content['abstract']['value'] == 'Paper abstract'
        assert note.content['_bibtex']['value'] == '''@article{
anonymous''' + str(datetime.datetime.fromtimestamp(note.cdate/1000).year) + '''paper,
title={Paper title 4},
author={Anonymous},
journal={Submitted to Transactions on Machine Learning Research},
year={''' + str(datetime.datetime.today().year) + '''},
url={https://openreview.net/forum?id=''' + note_id_4 + '''},
note={Rejected}
}'''

        deanonymize_authors_note = test_client.post_note_edit(invitation='TMLR/Paper4/-/Authors_De-Anonymization',
                            signatures=['TMLR/Paper4/Authors'],
                            note=Note(
                            content= {
                                'confirmation': { 'value': 'I want to reveal all author names on behalf of myself and my co-authors.' }
                            }))

        helpers.await_queue_edit(openreview_client, edit_id=deanonymize_authors_note['id'])

        note = openreview_client.get_note(note_id_4)
        assert note
        assert note.forum == note_id_4
        assert note.replyto is None
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/-/Edit', 'TMLR/-/Under_Review', 'TMLR/-/Rejected', 'TMLR/-/Authors_Release']
        assert note.readers == ['everyone']
        assert note.writers == ['TMLR', 'TMLR/Paper4/Authors']
        assert note.signatures == ['TMLR/Paper4/Authors']
        assert note.content['authorids']['value'] == ['~SomeFirstName_User1', '~Melissa_Eight1']
        assert note.content['authorids'].get('readers') == ['everyone']
        assert note.content['authors'].get('readers') == ['everyone']
        assert note.content['venue']['value'] == 'Rejected by TMLR'
        assert note.content['venueid']['value'] == 'TMLR/Rejected'
        assert note.content['title']['value'] == 'Paper title 4'
        assert note.content['abstract']['value'] == 'Paper abstract'
        assert note.content['_bibtex']['value'] == '''@article{
user''' + str(datetime.datetime.fromtimestamp(note.cdate/1000).year) + '''paper,
title={Paper title 4},
author={SomeFirstName User and Melissa Eight},
journal={Submitted to Transactions on Machine Learning Research},
year={''' + str(datetime.datetime.today().year) + '''},
url={https://openreview.net/forum?id=''' + note_id_4 + '''},
note={Rejected}
}'''

        ## Check invitations
        invitations = openreview_client.get_invitations(replyForum=note_id_4)
        assert len(invitations) == 10
        assert f"{venue_id}/-/Under_Review" in [i.id for i in invitations]
        assert f"{venue_id}/-/Withdrawn" in [i.id for i in invitations]
        assert f"{venue_id}/-/Desk_Rejected" in [i.id for i in invitations]
        assert f"{venue_id}/-/Rejected" in [i.id for i in invitations]
        assert f"{venue_id}/-/Retracted" in [i.id for i in invitations]
        assert f"{venue_id}/Paper4/-/Official_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper4/-/Public_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper4/-/Moderation" in [i.id for i in invitations]
        assert f"{venue_id}/Paper4/-/Authors_De-Anonymization" in [i.id for i in invitations]

        ## Check pending review edges
        edges_count = joelle_client.get_edges_count(invitation='TMLR/Reviewers/-/Pending_Reviews')
        assert edges_count == 5
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~David_Belanger1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Carlos_Mondragon1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Javier_Burroni1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Antony_Bal1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Hugo_Larochelle1')[0].weight == 0

    def test_eic_submission(self, journal, openreview_client, test_client, helpers):

        venue_id = journal.venue_id
        editor_in_chief_group_id = journal.get_editors_in_chief_id()
        raia_client = OpenReviewClient(username='raia@mail.com', password=helpers.strong_password)
        joelle_client = OpenReviewClient(username='joelle@mailseven.com', password=helpers.strong_password)
        cho_client = OpenReviewClient(username='kyunghyun@mail.com', password=helpers.strong_password)


        ## Reviewers
        david_client=OpenReviewClient(username='david@mailone.com', password=helpers.strong_password)
        javier_client=OpenReviewClient(username='javier@mailtwo.com', password=helpers.strong_password)
        carlos_client=OpenReviewClient(username='carlos@mailthree.com', password=helpers.strong_password)
        andrew_client=OpenReviewClient(username='andrewmc@mailfour.com', password=helpers.strong_password)
        hugo_client=OpenReviewClient(username='hugo@mailsix.com', password=helpers.strong_password)

        now = datetime.datetime.now()

        ## Post the submission 5
        submission_note_5 = raia_client.post_note_edit(invitation='TMLR/-/Submission',
            signatures=['~Raia_Hadsell1'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 5' },
                    'abstract': { 'value': 'Paper abstract' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight', 'Raia Hadsell']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1', '~Raia_Hadsell1']},
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'submission_length': { 'value': 'Regular submission (no more than 12 pages of main content)'}
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_5['id'])
        note_id_5=submission_note_5['note']['id']

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        openreview_client.get_invitation('TMLR/Paper5/Action_Editors/-/Recommendation')        

        # Assign Action Editor
        paper_assignment_edge = cho_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_5,
            tail='~Joelle_Pineau1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        messages = journal.client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Attention: you\'ve been assigned a submission authored by an EIC')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Joelle Pineau,

You have just been assigned a submission that is authored by one (or more) TMLR Editors-in-Chief. OpenReview is set up such that the EIC in question will not have access through OpenReview to the identity of the reviewers you'll be assigning. 

However, be mindful not to discuss the submission by email through TMLR's EIC mailing lists (tmlr@jmlr.org or tmlr-editors@jmlr.org), since all EICs receive these emails. Instead, if you need to reach out to EICs by email, only contact the non-conflicted EICs, directly.

We thank you for your cooperation.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''        

        ## try editing the assignmente edge being the author and get an error
        paper_assignment_edge.tail = '~Ryan_Adams1'
        paper_assignment_edge.readers=[venue_id, editor_in_chief_group_id, '~Ryan_Adams1']
        with pytest.raises(openreview.OpenReviewException, match=r'Authors can not edit assignments for this submission: 5'):
            raia_client.post_edge(paper_assignment_edge)
       
        
        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper5/-/Review_Approval',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 40)),
                duedate=openreview.tools.datetime_millis(datetime.datetime.now() - datetime.timedelta(days = 30)) + 2000,
                signatures=['TMLR']
            )
        )

        helpers.await_queue_edit(openreview_client, 'TMLR/Paper5/-/Review_Approval-0-2')

        messages = journal.client.get_messages(to= 'raia@mail.com', subject = '[TMLR] AE is late in performing a task for assigned paper 5: Paper title 5')
        assert len(messages) == 0

        joelle_paper5_anon_groups = joelle_client.get_groups(prefix=f'{venue_id}/Paper5/Action_Editor_.*', signatory='~Joelle_Pineau1')
        assert len(joelle_paper5_anon_groups) == 1
        joelle_paper5_anon_group = joelle_paper5_anon_groups[0]         

        ## Accept the submission 5
        under_review_note = joelle_client.post_note_edit(invitation= 'TMLR/Paper5/-/Review_Approval',
                                    signatures=[joelle_paper5_anon_group.id],
                                    note=Note(content={
                                        'under_review': { 'value': 'Appropriate for Review' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=under_review_note['id'])

        edits = openreview_client.get_note_edits(note_id=note_id_5, invitation='TMLR/-/Under_Review')

        helpers.await_queue_edit(openreview_client, edit_id=edits[0].id)

        ## Assign David Belanger
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper5/Action_Editors", '~David_Belanger1'],
            nonreaders=[f"{venue_id}/Paper5/Authors"],
            writers=[venue_id, f"{venue_id}/Paper5/Action_Editors"],
            signatures=[joelle_paper5_anon_group.id],
            head=note_id_5,
            tail='~David_Belanger1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ## Assign Carlos Mondragon
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper5/Action_Editors", '~Carlos_Mondragon1'],
            nonreaders=[f"{venue_id}/Paper5/Authors"],
            writers=[venue_id, f"{venue_id}/Paper5/Action_Editors"],
            signatures=[joelle_paper5_anon_group.id],
            head=note_id_5,
            tail='~Carlos_Mondragon1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ## Assign Javier Burroni
        ## try editing the assignmente edge being the author and get an error
        paper_assignment_edge = openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper5/Action_Editors", '~Javier_Burroni1'],
            nonreaders=[f"{venue_id}/Paper5/Authors"],
            writers=[venue_id, f"{venue_id}/Paper5/Action_Editors"],
            signatures=[joelle_paper5_anon_group.id],
            head=note_id_5,
            tail='~Javier_Burroni1',
            weight=1
        )
        with pytest.raises(openreview.OpenReviewException, match=r'Authors can not edit assignments for this submission: 5'):
            raia_client.post_edge(paper_assignment_edge)

        paper_assignment_edge = joelle_client.post_edge(paper_assignment_edge)
        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)      

        ## Post a review edit
        david_anon_groups=david_client.get_groups(prefix=f'{venue_id}/Paper5/Reviewer_.*', signatory='~David_Belanger1')
        assert len(david_anon_groups) == 1

        david_review_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper5/-/Review',
            signatures=[david_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'])

        ## Post a review edit
        javier_anon_groups=javier_client.get_groups(prefix=f'{venue_id}/Paper5/Reviewer_.*', signatory='~Javier_Burroni1')
        assert len(javier_anon_groups) == 1
        javier_review_note = javier_client.post_note_edit(invitation=f'{venue_id}/Paper5/-/Review',
            signatures=[javier_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'])

        ## Post a review edit
        carlos_anon_groups=carlos_client.get_groups(prefix=f'{venue_id}/Paper5/Reviewer_.*', signatory='~Carlos_Mondragon1')
        assert len(carlos_anon_groups) == 1
        carlos_review_note = carlos_client.post_note_edit(invitation=f'{venue_id}/Paper5/-/Review',
            signatures=[carlos_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'])


        invitation = cho_client.get_invitation(f'{venue_id}/Paper5/-/Official_Recommendation')
        #assert invitation.cdate > openreview.tools.datetime_millis(datetime.datetime.now())

        cho_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper5/-/Official_Recommendation',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now()),
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        ## Post a review recommendation
        official_recommendation_note = carlos_client.post_note_edit(invitation=f'{venue_id}/Paper5/-/Official_Recommendation',
            signatures=[carlos_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Reject' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        ## Post a review recommendation
        official_recommendation_note = javier_client.post_note_edit(invitation=f'{venue_id}/Paper5/-/Official_Recommendation',
            signatures=[javier_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Reject' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        ## Post a review recommendation
        official_recommendation_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper5/-/Official_Recommendation',
            signatures=[david_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Reject' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        reviews=openreview_client.get_notes(forum=note_id_5, invitation=f'{venue_id}/Paper5/-/Review', sort= 'number:asc')

        for review in reviews:
            signature=review.signatures[0]
            rating_note=joelle_client.post_note_edit(invitation=f'{signature}/-/Rating',
                signatures=[joelle_paper5_anon_group.id],
                note=Note(
                    content={
                        'rating': { 'value': 'Exceeds expectations' }
                    }
                )
            )
            helpers.await_queue_edit(openreview_client, edit_id=rating_note['id'])

        decision_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper5/-/Decision',
            signatures=[joelle_paper5_anon_group.id],
            note=Note(
                content={
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'Accept with minor revision' },
                    'audience': { 'value': 'No' },
                    'audience_explanation': { 'value': 'Accept with minor revision' },
                    'recommendation': { 'value': 'Accept with minor revision' },
                    'additional_comments': { 'value': 'This is a good paper' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=decision_note['id'])

        decision_note = joelle_client.get_note(decision_note['note']['id'])
        assert decision_note.readers == ['TMLR/Editors_In_Chief', f"{venue_id}/Paper5/Action_Editors"]

        ## EIC approves the decision
        with pytest.raises(openreview.OpenReviewException, match=r'NotInviteeError'):
            approval_note = raia_client.post_note_edit(invitation='TMLR/Paper5/-/Decision_Approval',
                                signatures=['TMLR/Editors_In_Chief'],
                                note=Note(
                                content= {
                                    'approval': { 'value': 'I approve the AE\'s decision.' },
                                    'comment_to_the_AE': { 'value': 'I agree with the AE' }
                                }))

        approval_note = cho_client.post_note_edit(invitation='TMLR/Paper5/-/Decision_Approval',
                            signatures=['TMLR/Editors_In_Chief'],
                            note=Note(
                            content= {
                                'approval': { 'value': 'I approve the AE\'s decision.' },
                                'comment_to_the_AE': { 'value': 'I agree with the AE' }
                            }))

        helpers.await_queue_edit(openreview_client, edit_id=approval_note['id'])

        decision_note = raia_client.get_note(decision_note.id)
        assert decision_note.readers == ['everyone']

        messages = journal.client.get_messages(to = 'raia@mail.com', subject = '[TMLR] Decision for your TMLR submission 5: Paper title 5')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Raia Hadsell,

We are happy to inform you that, based on the evaluation of the reviewers and the recommendation of the assigned Action Editor, your TMLR submission "5: Paper title 5" is accepted with minor revision.

To know more about the decision and submit the deanonymized camera ready version of your manuscript, please follow this link and click on button "Camera Ready Revision": https://openreview.net/forum?id={note_id_5}. Please submit the final version of your paper, including the minor revisions requested by the Action Editor, within 4 weeks ({(datetime.datetime.now() + datetime.timedelta(weeks = 4)).strftime("%b %d")}).

The Action Editor responsible for your submission will have provided a description of the revision expected for accepting your final manuscript.

In addition to your final manuscript, we strongly encourage you to submit a link to 1) code associated with your and 2) a short video presentation of your work. You can provide these links to the corresponding entries on the revision page.

For more details and guidelines on the TMLR review process, visit jmlr.org/tmlr.

We thank you for your contribution to TMLR and congratulate you for your successful submission!

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''
        ## Expire review invitations to the jobs are cancelled
        withdraw_note = raia_client.post_note_edit(invitation='TMLR/Paper5/-/Withdrawal',
                                    signatures=[f'{venue_id}/Paper5/Authors'],
                                    note=Note(
                                        content={
                                            'withdrawal_confirmation': { 'value': 'I have read and agree with the venue\'s withdrawal policy on behalf of myself and my co-authors.' },
                                        }
                                    ))
        
        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'], process_index=0)
        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'], process_index=0)
        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'], process_index=0)

        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'], process_index=1)
        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'], process_index=1)
        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'], process_index=1)


    def test_withdraw_submission(self, journal, openreview_client, helpers):

        venue_id = journal.venue_id
        editor_in_chief_group_id = journal.get_editors_in_chief_id()
        test_client = OpenReviewClient(username='test@mail.com', password=helpers.strong_password)
        raia_client = OpenReviewClient(username='raia@mail.com', password=helpers.strong_password)
        joelle_client = OpenReviewClient(username='joelle@mailseven.com', password=helpers.strong_password)
        cho_client = OpenReviewClient(username='kyunghyun@mail.com', password=helpers.strong_password)


        ## Reviewers
        david_client=OpenReviewClient(username='david@mailone.com', password=helpers.strong_password)
        javier_client=OpenReviewClient(username='javier@mailtwo.com', password=helpers.strong_password)
        carlos_client=OpenReviewClient(username='carlos@mailthree.com', password=helpers.strong_password)
        andrew_client=OpenReviewClient(username='andrewmc@mailfour.com', password=helpers.strong_password)
        hugo_client=OpenReviewClient(username='hugo@mailsix.com', password=helpers.strong_password)

        now = datetime.datetime.now()

        ## Post the submission 6
        submission_note_6 = test_client.post_note_edit(invitation='TMLR/-/Submission',
            signatures=['~SomeFirstName_User1'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 6' },
                    'abstract': { 'value': 'Paper abstract' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1']},
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'submission_length': { 'value': 'Regular submission (no more than 12 pages of main content)'}
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_6['id'])
        note_id_6=submission_note_6['note']['id']

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        openreview_client.get_invitation('TMLR/Paper6/Action_Editors/-/Recommendation')        

        # Assign Action Editor
        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_6,
            tail='~Joelle_Pineau1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        joelle_paper6_anon_groups = joelle_client.get_groups(prefix=f'{venue_id}/Paper6/Action_Editor_.*', signatory='~Joelle_Pineau1')
        assert len(joelle_paper6_anon_groups) == 1
        joelle_paper6_anon_group = joelle_paper6_anon_groups[0]         

        ## Accept the submission 6
        under_review_note = joelle_client.post_note_edit(invitation= 'TMLR/Paper6/-/Review_Approval',
                                    signatures=[joelle_paper6_anon_group.id],
                                    note=Note(content={
                                        'under_review': { 'value': 'Appropriate for Review' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=under_review_note['id'])

        edits = openreview_client.get_note_edits(note_id=note_id_6, invitation='TMLR/-/Under_Review')

        helpers.await_queue_edit(openreview_client, edit_id=edits[0].id)

        ## Assign David Belanger
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper6/Action_Editors", '~David_Belanger1'],
            nonreaders=[f"{venue_id}/Paper6/Authors"],
            writers=[venue_id, f"{venue_id}/Paper6/Action_Editors"],
            signatures=[joelle_paper6_anon_group.id],
            head=note_id_6,
            tail='~David_Belanger1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ## Assign Carlos Mondragon
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper6/Action_Editors", '~Carlos_Mondragon1'],
            nonreaders=[f"{venue_id}/Paper6/Authors"],
            writers=[venue_id, f"{venue_id}/Paper6/Action_Editors"],
            signatures=[joelle_paper6_anon_group.id],
            head=note_id_6,
            tail='~Carlos_Mondragon1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ## Assign Javier Burroni
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper6/Action_Editors", '~Javier_Burroni1'],
            nonreaders=[f"{venue_id}/Paper6/Authors"],
            writers=[venue_id, f"{venue_id}/Paper6/Action_Editors"],
            signatures=[joelle_paper6_anon_group.id],
            head=note_id_6,
            tail='~Javier_Burroni1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ## Post a review edit
        david_anon_groups=david_client.get_groups(prefix=f'{venue_id}/Paper6/Reviewer_.*', signatory='~David_Belanger1')
        assert len(david_anon_groups) == 1

        david_review_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper6/-/Review',
            signatures=[david_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'])

        ## Post a review edit
        javier_anon_groups=javier_client.get_groups(prefix=f'{venue_id}/Paper6/Reviewer_.*', signatory='~Javier_Burroni1')
        assert len(javier_anon_groups) == 1
        javier_review_note = javier_client.post_note_edit(invitation=f'{venue_id}/Paper6/-/Review',
            signatures=[javier_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' } 
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'])

        ## Post a review edit
        carlos_anon_groups=carlos_client.get_groups(prefix=f'{venue_id}/Paper6/Reviewer_.*', signatory='~Carlos_Mondragon1')
        assert len(carlos_anon_groups) == 1
        carlos_review_note = carlos_client.post_note_edit(invitation=f'{venue_id}/Paper6/-/Review',
            signatures=[carlos_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'])


        invitation = cho_client.get_invitation(f'{venue_id}/Paper6/-/Official_Recommendation')
        #assert invitation.cdate > openreview.tools.datetime_millis(datetime.datetime.now())

        cho_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper6/-/Official_Recommendation',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now()),
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        ## Post a review recommendation
        official_recommendation_note = carlos_client.post_note_edit(invitation=f'{venue_id}/Paper6/-/Official_Recommendation',
            signatures=[carlos_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Reject' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        ## Post a review recommendation
        official_recommendation_note = javier_client.post_note_edit(invitation=f'{venue_id}/Paper6/-/Official_Recommendation',
            signatures=[javier_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Reject' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        ## Post a review recommendation
        official_recommendation_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper6/-/Official_Recommendation',
            signatures=[david_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Reject' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        reviews=openreview_client.get_notes(forum=note_id_6, invitation=f'{venue_id}/Paper6/-/Review', sort= 'number:asc')

        for review in reviews:
            signature=review.signatures[0]
            rating_note=joelle_client.post_note_edit(invitation=f'{signature}/-/Rating',
                signatures=[joelle_paper6_anon_group.id],
                note=Note(
                    content={
                        'rating': { 'value': 'Exceeds expectations' }
                    }
                )
            )
            helpers.await_queue_edit(openreview_client, edit_id=rating_note['id'])

        ## Withdraw the submission 6
        withdraw_note = test_client.post_note_edit(invitation='TMLR/Paper6/-/Withdrawal',
                                    signatures=[f'{venue_id}/Paper6/Authors'],
                                    note=Note(
                                        content={
                                            'withdrawal_confirmation': { 'value': 'I have read and agree with the venue\'s withdrawal policy on behalf of myself and my co-authors.' },
                                        }
                                    ))

        helpers.await_queue_edit(openreview_client, edit_id=withdraw_note['id'])

        note = test_client.get_note(note_id_6)
        assert note
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/-/Edit', 'TMLR/-/Under_Review', 'TMLR/-/Withdrawn']
        assert note.readers == ['everyone']
        assert note.writers == ['TMLR', 'TMLR/Paper6/Authors']
        assert note.signatures == ['TMLR/Paper6/Authors']
        assert note.content['authorids']['value'] == ['~SomeFirstName_User1', '~Melissa_Eight1']
        assert note.content['venue']['value'] == 'Withdrawn by Authors'
        assert note.content['venueid']['value'] == 'TMLR/Withdrawn_Submission'

        edits = openreview_client.get_note_edits(note_id=note_id_6, invitation='TMLR/-/Withdrawn')
        assert len(edits) == 1
        helpers.await_queue_edit(openreview_client, edit_id=edits[0].id)

        ## Check invitations
        invitations = openreview_client.get_invitations(replyForum=note_id_6)
        assert len(invitations) == 10
        assert f"{venue_id}/-/Under_Review" in [i.id for i in invitations]
        assert f"{venue_id}/-/Withdrawn" in [i.id for i in invitations]
        assert f"{venue_id}/-/Desk_Rejected" in [i.id for i in invitations]
        assert f"{venue_id}/-/Rejected" in [i.id for i in invitations]
        assert f"{venue_id}/Paper6/-/Official_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper6/-/Public_Comment" in [i.id for i in invitations]
        assert f"{venue_id}/Paper6/-/Moderation" in [i.id for i in invitations]

        messages = journal.client.get_messages(subject = '[TMLR] Authors have withdrawn TMLR submission 6: Paper title 6')
        assert len(messages) == 4

        deanonymize_authors_note = test_client.post_note_edit(invitation='TMLR/Paper6/-/Authors_De-Anonymization',
                            signatures=['TMLR/Paper6/Authors'],
                            note=Note(
                            content= {
                                'confirmation': { 'value': 'I want to reveal all author names on behalf of myself and my co-authors.' }
                            }))

        helpers.await_queue_edit(openreview_client, edit_id=deanonymize_authors_note['id'])

        note = openreview_client.get_note(note_id_6)
        assert note
        assert note.forum == note_id_6
        assert note.replyto is None
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/-/Edit', 'TMLR/-/Under_Review', 'TMLR/-/Withdrawn', 'TMLR/-/Authors_Release']
        assert note.readers == ['everyone']
        assert note.writers == ['TMLR', 'TMLR/Paper6/Authors']
        assert note.signatures == ['TMLR/Paper6/Authors']
        assert note.content['authorids']['value'] == ['~SomeFirstName_User1', '~Melissa_Eight1']
        assert note.content['authorids'].get('readers') == ['everyone']
        assert note.content['authors'].get('readers') == ['everyone']
        assert note.content['venue']['value'] == 'Withdrawn by Authors'
        assert note.content['venueid']['value'] == 'TMLR/Withdrawn_Submission'
        assert note.content['title']['value'] == 'Paper title 6'
        assert note.content['abstract']['value'] == 'Paper abstract'
        assert note.content['_bibtex']['value'] == '''@article{
user''' + str(datetime.datetime.fromtimestamp(note.cdate/1000).year) + '''paper,
title={Paper title 6},
author={SomeFirstName User and Melissa Eight},
journal={Submitted to Transactions on Machine Learning Research},
year={''' + str(datetime.datetime.today().year) + '''},
url={https://openreview.net/forum?id=''' + note_id_6 + '''},
note={Withdrawn}
}'''

        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'], process_index=0)
        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'], process_index=0)
        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'], process_index=0)

        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'], process_index=1)
        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'], process_index=1)
        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'], process_index=1)


    def test_submitted_submission(self, journal, openreview_client, helpers):

        test_client = OpenReviewClient(username='test@mail.com', password=helpers.strong_password)
        venue_id = journal.venue_id
        raia_client = OpenReviewClient(username='raia@mail.com', password=helpers.strong_password)
        joelle_client = OpenReviewClient(username='joelle@mailseven.com', password=helpers.strong_password)
        editor_in_chief_group_id = journal.get_editors_in_chief_id()

        ## Post the submission 7
        submission_note_7 = test_client.post_note_edit(invitation='TMLR/-/Submission',
            signatures=['~SomeFirstName_User1'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 7' },
                    'abstract': { 'value': 'Paper abstract' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1']},
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'submission_length': { 'value': 'Long submission (more than 12 pages of main content)'}
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_7['id'])
        note_id_7 = submission_note_7['note']['id']

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        openreview_client.get_invitation('TMLR/Paper7/Action_Editors/-/Recommendation')        

        # Assign Action Editor
        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_7,
            tail='~Joelle_Pineau1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        joelle_paper7_anon_groups = joelle_client.get_groups(prefix=f'{venue_id}/Paper7/Action_Editor_.*', signatory='~Joelle_Pineau1')
        assert len(joelle_paper7_anon_groups) == 1
        joelle_paper7_anon_group = joelle_paper7_anon_groups[0] 

        ## Accept the submission 7
        under_review_note = joelle_client.post_note_edit(invitation= 'TMLR/Paper7/-/Review_Approval',
                                    signatures=[joelle_paper7_anon_group.id],
                                    note=Note(content={
                                        'under_review': { 'value': 'Appropriate for Review' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=under_review_note['id'])

        edits = openreview_client.get_note_edits(note_id=note_id_7, invitation='TMLR/-/Under_Review')

        helpers.await_queue_edit(openreview_client, edit_id=edits[0].id)

        ## Assign David Belanger
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper7/Action_Editors", '~David_Belanger1'],
            nonreaders=[f"{venue_id}/Paper7/Authors"],
            writers=[venue_id, f"{venue_id}/Paper7/Action_Editors"],
            signatures=[joelle_paper7_anon_group.id],
            head=note_id_7,
            tail='~David_Belanger1',
            weight=1
        ))

        ## Ask solicit review with a conflict
        tom_client = OpenReviewClient(username='tom@mail.com', password=helpers.strong_password)
        Volunteer_to_Review_note = tom_client.post_note_edit(invitation=f'{venue_id}/Paper7/-/Volunteer_to_Review',
            signatures=['~Tom_Rain1'],
            note=Note(
                content={
                    'solicit': { 'value': 'I solicit to review this paper.' },
                    'comment': { 'value': 'I can review this paper.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=Volunteer_to_Review_note['id'])
        assert 'TMLR/Editors_In_Chief' in Volunteer_to_Review_note['note']['readers']

        ## Post a response
        Volunteer_to_Review_approval_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper7/-/~Tom_Rain1_Volunteer_to_Review_Approval',
            signatures=[joelle_paper7_anon_group.id],
            note=Note(
                forum=note_id_7,
                replyto=Volunteer_to_Review_note['note']['id'],
                content={
                    'decision': { 'value': 'No, I decline the solicit review.' },
                    'comment': { 'value': 'Sorry, all the reviewers were assigned.' }
                }
            )
        )
        assert 'TMLR/Editors_In_Chief' in Volunteer_to_Review_approval_note['note']['readers']

        helpers.await_queue_edit(openreview_client, edit_id=Volunteer_to_Review_approval_note['id'])

        messages = journal.client.get_messages(to = 'tom@mail.com', subject = '[TMLR] Request to review TMLR submission "7: Paper title 7" was not accepted')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Tom Rain,

This is to inform you that your request to act as a reviewer for TMLR submission 7: Paper title 7 was not accepted by the Action Editor (AE). If you would like to know more about the reason behind this decision, you can click here: https://openreview.net/forum?id={note_id_7}&noteId={Volunteer_to_Review_approval_note['note']['id']}.

Respectfully,

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''

        ## Solicit review to more than 2 papers
        peter_client=OpenReviewClient(username='petersnow@yahoo.com', password=helpers.strong_password)
        Volunteer_to_Review_note = peter_client.post_note_edit(invitation=f'{venue_id}/Paper7/-/Volunteer_to_Review',
            signatures=['~Peter_Snow1'],
            note=Note(
                content={
                    'solicit': { 'value': 'I solicit to review this paper.' },
                    'comment': { 'value': 'I can review this paper.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=Volunteer_to_Review_note['id'])

        ## Post a response
        Volunteer_to_Review_approval_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper7/-/~Peter_Snow1_Volunteer_to_Review_Approval',
            signatures=[joelle_paper7_anon_group.id],
            note=Note(
                forum=note_id_7,
                replyto=Volunteer_to_Review_note['note']['id'],
                content={
                    'decision': { 'value': 'Yes, I approve the solicit review.' },
                    'comment': { 'value': 'thanks!' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=Volunteer_to_Review_approval_note['id'])

        ## Post the submission 8
        submission_note_8 = test_client.post_note_edit(invitation='TMLR/-/Submission',
            signatures=['~SomeFirstName_User1'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 8' },
                    'abstract': { 'value': 'Paper abstract' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1']},
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'submission_length': { 'value': 'Long submission (more than 12 pages of main content)'}
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_8['id'])
        note_id_8 = submission_note_8['note']['id']

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        openreview_client.get_invitation('TMLR/Paper8/Action_Editors/-/Recommendation')        

        # Assign Action Editor
        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_8,
            tail='~Joelle_Pineau1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        joelle_paper8_anon_groups = joelle_client.get_groups(prefix=f'{venue_id}/Paper8/Action_Editor_.*', signatory='~Joelle_Pineau1')
        assert len(joelle_paper8_anon_groups) == 1
        joelle_paper8_anon_group = joelle_paper8_anon_groups[0]         

        ## Accept the submission 8
        under_review_note = joelle_client.post_note_edit(invitation= 'TMLR/Paper8/-/Review_Approval',
                                    signatures=[joelle_paper8_anon_group.id],
                                    note=Note(content={
                                        'under_review': { 'value': 'Appropriate for Review' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=under_review_note['id'])

        edits = openreview_client.get_note_edits(note_id=note_id_8, invitation='TMLR/-/Under_Review')

        helpers.await_queue_edit(openreview_client, edit_id=edits[0].id)

        ## Assign David Belanger should throw an error
        with pytest.raises(openreview.OpenReviewException, match=r'Can not add assignment, reviewer ~David_Belanger1 has 1 pending reviews.'):
            paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
                readers=[venue_id, f"{venue_id}/Paper8/Action_Editors", '~David_Belanger1'],
                nonreaders=[f"{venue_id}/Paper8/Authors"],
                writers=[venue_id, f"{venue_id}/Paper8/Action_Editors"],
                signatures=[joelle_paper8_anon_group.id],
                head=note_id_8,
                tail='~David_Belanger1',
                weight=1
            ))

        david_client = OpenReviewClient(username='david@mailone.com', password=helpers.strong_password)
        volunteer_to_review_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper8/-/Volunteer_to_Review',
            signatures=['~David_Belanger1'],
            note=Note(
                content={
                    'solicit': { 'value': 'I solicit to review this paper.' },
                    'comment': { 'value': 'I can review this paper.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=volunteer_to_review_note['id'])

        volunteer_to_review_approval_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper8/-/~David_Belanger1_Volunteer_to_Review_Approval',
            signatures=[joelle_paper8_anon_group.id],
            note=Note(
                forum=note_id_8,
                replyto=volunteer_to_review_note['note']['id'],
                content={
                    'decision': { 'value': 'Yes, I approve the solicit review.' },
                    'comment': { 'value': 'thanks!' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=volunteer_to_review_approval_note['id'])
        assignment_edge = openreview_client.get_edges(invitation='TMLR/Reviewers/-/Assignment', head=note_id_8, tail='~David_Belanger1')[0]
        helpers.await_queue_edit(openreview_client, edit_id=assignment_edge.id)                

        Volunteer_to_Review_note = peter_client.post_note_edit(invitation=f'{venue_id}/Paper8/-/Volunteer_to_Review',
            signatures=['~Peter_Snow1'],
            note=Note(
                content={
                    'solicit': { 'value': 'I solicit to review this paper.' },
                    'comment': { 'value': 'I can review this paper.' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=Volunteer_to_Review_note['id'])

        ## Post a response
        Volunteer_to_Review_approval_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper8/-/~Peter_Snow1_Volunteer_to_Review_Approval',
            signatures=[joelle_paper8_anon_group.id],
            note=Note(
                forum=note_id_8,
                replyto=Volunteer_to_Review_note['note']['id'],
                content={
                    'decision': { 'value': 'Yes, I approve the solicit review.' },
                    'comment': { 'value': 'thanks!' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=Volunteer_to_Review_approval_note['id'])
        assignment_edge = openreview_client.get_edges(invitation='TMLR/Reviewers/-/Assignment', head=note_id_8, tail='~Peter_Snow1')[0]
        helpers.await_queue_edit(openreview_client, edit_id=assignment_edge.id)

        ## Check pending review edges
        edges = joelle_client.get_edges_count(invitation='TMLR/Reviewers/-/Pending_Reviews')
        assert edges == 5
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Carlos_Mondragon1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Javier_Burroni1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~David_Belanger1')[0].weight == 2
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Hugo_Larochelle1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Antony_Bal1')[0].weight == 0

        note = openreview_client.get_note(note_id_7)
        journal.invitation_builder.expire_paper_invitations(note)

        ## Check pending review edges
        edges = joelle_client.get_edges_count(invitation='TMLR/Reviewers/-/Pending_Reviews')
        assert edges == 5
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Carlos_Mondragon1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Javier_Burroni1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~David_Belanger1')[0].weight == 1
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Hugo_Larochelle1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Antony_Bal1')[0].weight == 0

        note = openreview_client.get_note(note_id_8)
        journal.invitation_builder.expire_paper_invitations(note)

        ## Check pending review edges
        edges = joelle_client.get_edges_count(invitation='TMLR/Reviewers/-/Pending_Reviews')
        assert edges == 5
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Carlos_Mondragon1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Javier_Burroni1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~David_Belanger1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Hugo_Larochelle1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Antony_Bal1')[0].weight == 0

        # Assign another Action Editor and the submission should be updated
        current_assignment = raia_client.get_edges(invitation='TMLR/Action_Editors/-/Assignment', head=note_id_8)[0]
        current_assignment.ddate = openreview.tools.datetime_millis(datetime.datetime.now())
        raia_client.post_edge(current_assignment)

        helpers.await_queue_edit(openreview_client, edit_id=current_assignment.id, count=2)

        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Samy_Bengio1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_8,
            tail='~Samy_Bengio1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        submission = raia_client.get_note(note_id_8)
        assert '~Samy_Bengio1' == submission.content['assigned_action_editor']['value']

        journal.invitation_builder.expire_paper_invitations(submission)        


    def test_desk_rejected_submission_by_eic(self, journal, openreview_client, helpers):

        test_client = OpenReviewClient(username='test@mail.com', password=helpers.strong_password)
        venue_id = journal.venue_id
        raia_client = OpenReviewClient(username='raia@mail.com', password=helpers.strong_password)
        joelle_client = OpenReviewClient(username='joelle@mailseven.com', password=helpers.strong_password)
        editor_in_chief_group_id = journal.get_editors_in_chief_id()

        ## Post the submission 9
        submission_note_9 = test_client.post_note_edit(invitation='TMLR/-/Submission',
            signatures=['~SomeFirstName_User1'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 9' },
                    'abstract': { 'value': 'Paper abstract' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1']},
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'submission_length': { 'value': 'Regular submission (no more than 12 pages of main content)'}
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_9['id'])
        note_id_9 = submission_note_9['note']['id']

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        openreview_client.get_invitation('TMLR/Paper9/Action_Editors/-/Recommendation')        

        ## Desk Reject by EIC
        desk_reject_note = raia_client.post_note_edit(invitation= 'TMLR/Paper9/-/Desk_Rejection',
                                    signatures=[f'{venue_id}/Editors_In_Chief'],
                                    note=Note(content={
                                        'desk_reject_comments': { 'value': 'PDF is not anonymized.' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=desk_reject_note['id'])

        note = openreview_client.get_note(note_id_9)
        assert note
        assert note.forum == note_id_9
        assert note.replyto is None
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/-/Desk_Rejected']
        assert note.readers == ['TMLR', 'TMLR/Paper9/Action_Editors', 'TMLR/Paper9/Authors']
        assert note.writers == ['TMLR', 'TMLR/Paper9/Action_Editors']
        assert note.signatures == ['TMLR/Paper9/Authors']
        assert note.content['authorids']['value'] == ['~SomeFirstName_User1', '~Melissa_Eight1']
        assert note.content['venue']['value'] == 'Desk rejected by TMLR'
        assert note.content['venueid']['value'] == 'TMLR/Desk_Rejected'
        assert note.content['title']['value'] == 'Paper title 9'
        assert note.content['abstract']['value'] == 'Paper abstract'

        messages = journal.client.get_messages(to = 'test@mail.com', subject = '[TMLR] Decision for your TMLR submission 9: Paper title 9')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi SomeFirstName User,

We are sorry to inform you that, after consideration by the Editors-in-Chief, your TMLR submission "9: Paper title 9" has been rejected without further review.

Cases of desk rejection include submissions that are not anonymized, submissions that do not use the unmodified TMLR stylefile and submissions that clearly overlap with work already published in proceedings (or currently under review for publication).

To know more about the decision, please follow this link: https://openreview.net/forum?id={note_id_9}

For more details and guidelines on the TMLR review process, visit jmlr.org/tmlr.

The TMLR Editors-in-Chief


Please note that responding to this email will direct your reply to tmlr@jmlr.org.
'''


        note = openreview_client.get_note(note_id_9)
        journal.invitation_builder.expire_paper_invitations(note)

    def test_resubmission(self, journal, openreview_client, helpers):

        test_client = OpenReviewClient(username='test@mail.com', password=helpers.strong_password)
        venue_id = journal.venue_id
        raia_client = OpenReviewClient(username='raia@mail.com', password=helpers.strong_password)
        joelle_client = OpenReviewClient(username='joelle@mailseven.com', password=helpers.strong_password)
        editor_in_chief_group_id = journal.get_editors_in_chief_id()

        rejected_submission = openreview_client.get_notes(invitation='TMLR/-/Submission', number=4)[0]
        ## Resubmit rejected paper
        submission_note_10 = test_client.post_note_edit(invitation='TMLR/-/Submission',
            signatures=['~SomeFirstName_User1'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 4' },
                    'abstract': { 'value': 'Paper abstract' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1']},
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'submission_length': { 'value': 'Long submission (more than 12 pages of main content)'},
                    'previous_TMLR_submission_url': { 'value': f'https://openreview.net/forum?id={rejected_submission.id}' }
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_10['id'])
        note_id_10 = submission_note_10['note']['id']

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        openreview_client.get_invitation('TMLR/Paper10/Action_Editors/-/Recommendation')        

        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_10,
            tail='~Joelle_Pineau1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        joelle_paper10_anon_groups = joelle_client.get_groups(prefix=f'{venue_id}/Paper10/Action_Editor_.*', signatory='~Joelle_Pineau1')
        assert len(joelle_paper10_anon_groups) == 1
        joelle_paper10_anon_group = joelle_paper10_anon_groups[0]         

        ## Accept the submission 8
        under_review_note = joelle_client.post_note_edit(invitation= 'TMLR/Paper10/-/Review_Approval',
                                    signatures=[joelle_paper10_anon_group.id],
                                    note=Note(content={
                                        'under_review': { 'value': 'Appropriate for Review' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=under_review_note['id'])

        edits = openreview_client.get_note_edits(note_id=note_id_10, invitation='TMLR/-/Under_Review')

        helpers.await_queue_edit(openreview_client, edit_id=edits[0].id)

        ## Assign David Belanger because of being the reviewer of the previous submission
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper10/Action_Editors", '~David_Belanger1'],
            nonreaders=[f"{venue_id}/Paper10/Authors"],
            writers=[venue_id, f"{venue_id}/Paper10/Action_Editors"],
            signatures=[joelle_paper10_anon_group.id],
            head=note_id_10,
            tail='~David_Belanger1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ## Check pending review edges
        edges = joelle_client.get_edges_count(invitation='TMLR/Reviewers/-/Pending_Reviews')
        assert edges == 5
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Carlos_Mondragon1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Javier_Burroni1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~David_Belanger1')[0].weight == 1
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Hugo_Larochelle1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Antony_Bal1')[0].weight == 0


        note = openreview_client.get_note(note_id_10)
        journal.invitation_builder.expire_paper_invitations(note)

        ## Check pending review edges
        edges = joelle_client.get_edges_count(invitation='TMLR/Reviewers/-/Pending_Reviews')
        assert edges == 5
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Carlos_Mondragon1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Javier_Burroni1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~David_Belanger1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Hugo_Larochelle1')[0].weight == 0
        assert joelle_client.get_edges(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~Antony_Bal1')[0].weight == 0


    def test_submission_with_many_authors(self, journal, openreview_client, test_client, helpers):

        test_client = OpenReviewClient(username='test@mail.com', password=helpers.strong_password)
        venue_id = journal.venue_id
        raia_client = OpenReviewClient(username='raia@mail.com', password=helpers.strong_password)
        joelle_client = OpenReviewClient(username='joelle@mailseven.com', password=helpers.strong_password)
        editor_in_chief_group_id = journal.get_editors_in_chief_id()

        authors = ['SomeFirstName User']
        authorids = ['~SomeFirstName_User1']
        for i in alc:
            for j in alc[:5]:
                helpers.create_user(f'author_{i}{j}@mail.com', 'Author', f'TMLR {i}{j}')
                authors.append(f'Author TMLR {i}{j}')
                authorids.append(f'~Author_TMLR_{i}{j}1')
        
        submission_note_11 = test_client.post_note_edit(invitation='TMLR/-/Submission',
            signatures=['~SomeFirstName_User1'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 4' },
                    'abstract': { 'value': 'Paper abstract' },
                    'authors': { 'value': authors},
                    'authorids': { 'value': authorids},
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'submission_length': { 'value': 'Long submission (more than 12 pages of main content)'},
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_11['id'])
        note_id_11 = submission_note_11['note']['id']

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        openreview_client.get_invitation('TMLR/Paper11/Action_Editors/-/Recommendation')        

        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_11,
            tail='~Joelle_Pineau1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        note = openreview_client.get_note(note_id_11)

        joelle_paper11_anon_groups = joelle_client.get_groups(prefix=f'{venue_id}/Paper11/Action_Editor_.*', signatory='~Joelle_Pineau1')
        assert len(joelle_paper11_anon_groups) == 1
        joelle_paper11_anon_group = joelle_paper11_anon_groups[0]         

        ## Accept the submission 8
        under_review_note = joelle_client.post_note_edit(invitation= f'TMLR/Paper{note.number}/-/Review_Approval',
                                    signatures=[joelle_paper11_anon_group.id],
                                    note=Note(content={
                                        'under_review': { 'value': 'Appropriate for Review' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=under_review_note['id'])

        edits = openreview_client.get_note_edits(note_id_11, sort='tcdate:desc')
        assert len(edits) == 3
        assert edits[0].invitation == 'TMLR/-/Under_Review'
        helpers.await_queue_edit(openreview_client, edit_id=edits[0].id)
              
        journal.invitation_builder.expire_paper_invitations(note)

        invitation = openreview_client.get_invitation('TMLR/Paper11/Reviewers/-/Assignment')
        assert invitation.expdate is not None


    def test_decline_desk_rejection(self, journal, openreview_client, helpers):

        venue_id = journal.venue_id
        editor_in_chief_group_id = journal.get_editors_in_chief_id()
        test_client = OpenReviewClient(username='test@mail.com', password=helpers.strong_password)
        raia_client = OpenReviewClient(username='raia@mail.com', password=helpers.strong_password)
        joelle_client = OpenReviewClient(username='joelle@mailseven.com', password=helpers.strong_password)        

        ## Post the submission 12
        submission_note_12 = test_client.post_note_edit(invitation='TMLR/-/Submission',
            signatures=['~SomeFirstName_User1'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 12' },
                    'abstract': { 'value': 'Paper abstract' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1']},
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'submission_length': { 'value': 'Long submission (more than 12 pages of main content)'}
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_12['id'])
        note_id_12=submission_note_12['note']['id']

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        openreview_client.get_invitation('TMLR/Paper12/Action_Editors/-/Recommendation')        

        # Assign Action Editor
        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_12,
            tail='~Joelle_Pineau1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        joelle_paper12_anon_groups = joelle_client.get_groups(prefix=f'{venue_id}/Paper12/Action_Editor_.*', signatory='~Joelle_Pineau1')
        assert len(joelle_paper12_anon_groups) == 1
        joelle_paper12_anon_group = joelle_paper12_anon_groups[0]         

        desk_reject_note = joelle_client.post_note_edit(invitation= 'TMLR/Paper12/-/Review_Approval',
                                    signatures=[joelle_paper12_anon_group.id],
                                    note=Note(content={
                                        'under_review': { 'value': 'Desk Reject' },
                                        'comment': { 'value': 'this paper is not ready' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=desk_reject_note['id'])
        
        assert openreview_client.get_invitation(f"{venue_id}/Paper12/-/Desk_Rejection_Approval")
        approval_note = raia_client.post_note_edit(invitation='TMLR/Paper12/-/Desk_Rejection_Approval',
                            signatures=[f"{venue_id}/Editors_In_Chief"],
                            note=Note(
                                signatures=[f"{venue_id}/Editors_In_Chief"],
                                forum=note_id_12,
                                replyto=desk_reject_note['note']['id'],
                                content= {
                                    'approval': { 'value': 'I don\'t approve the AE\'s decision. Submission should be appropriate for review.' }
                                 }
                            ))
        
        helpers.await_queue_edit(openreview_client, edit_id=approval_note['id'])
        
        notes = openreview_client.get_notes(invitation='TMLR/Paper12/-/Review_Approval', signature='TMLR/Editors_In_Chief')
        edits = openreview_client.get_note_edits(notes[0].id)
        edit = [e for e in edits if 'TMLR/Paper12/-/Review_Approval' == e.invitation][0]
        helpers.await_queue_edit(openreview_client, edit_id=edit.id)

        note = joelle_client.get_note(note_id_12)
        assert note
        assert note.odate
        assert note.invitations == ['TMLR/-/Submission', 'TMLR/-/Edit', 'TMLR/-/Under_Review']
        assert note.readers == ['everyone']
        assert note.writers == ['TMLR', 'TMLR/Paper12/Authors']
        assert note.signatures == ['TMLR/Paper12/Authors']
        assert note.content['authorids']['value'] == ['~SomeFirstName_User1', '~Melissa_Eight1']
        assert note.content['venue']['value'] == 'Under review for TMLR'
        assert note.content['venueid']['value'] == 'TMLR/Under_Review'
        assert note.content['assigned_action_editor']['value'] == '~Joelle_Pineau1'
        assert note.content['_bibtex']['value'] == '''@article{
anonymous''' + str(datetime.datetime.fromtimestamp(note.cdate/1000).year) + '''paper,
title={Paper title 12},
author={Anonymous},
journal={Submitted to Transactions on Machine Learning Research},
year={''' + str(datetime.datetime.today().year) + '''},
url={https://openreview.net/forum?id=''' + note_id_12 + '''},
note={Under review}
}'''                                                                              

        edits = openreview_client.get_note_edits(note.id, invitation='TMLR/-/Under_Review')
        helpers.await_queue_edit(openreview_client, edit_id=edits[0].id)

        messages = openreview_client.get_messages(to = 'joelle@mailseven.com', subject = '[TMLR] Perform reviewer assignments for TMLR submission 12: Paper title 12')
        assert len(messages) == 1

        messages = openreview_client.get_messages(subject='[TMLR] Review Approval edited on submission 12: Paper title 12')
        assert len(messages) == 3, messages
        
        messages = openreview_client.get_messages(to = 'melissa@maileight.com', subject = '[TMLR] Review Approval edited on submission 12: Paper title 12')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'Hi Melissa Eight,\n\nA review approval has been edited on your submission.\n\nSubmission: Paper title 12\nUnder review: Appropriate for Review\nComment: \n\nTo view the review approval, click here: https://openreview.net/forum?id={note_id_12}&noteId={notes[0].id}\n\n\nPlease note that responding to this email will direct your reply to tmlr@jmlr.org.\n'

        note = openreview_client.get_note(note_id_12)
        journal.invitation_builder.expire_paper_invitations(note)


    def test_archived_action_editor(self, journal, openreview_client, test_client, helpers):

        venue_id = journal.venue_id
        test_client = OpenReviewClient(username='test@mail.com', password=helpers.strong_password)
        raia_client = OpenReviewClient(username='raia@mail.com', password=helpers.strong_password)
        joelle_client = OpenReviewClient(username='joelle@mailseven.com', password=helpers.strong_password)


        ## Reviewers
        david_client=OpenReviewClient(username='david@mailone.com', password=helpers.strong_password)
        javier_client=OpenReviewClient(username='javier@mailtwo.com', password=helpers.strong_password)
        carlos_client=OpenReviewClient(username='carlos@mailthree.com', password=helpers.strong_password)
        andrew_client=OpenReviewClient(username='andrewmc@mailfour.com', password=helpers.strong_password)
        hugo_client=OpenReviewClient(username='hugo@mailsix.com', password=helpers.strong_password)

        ## Post the submission 13
        submission_note_13 = test_client.post_note_edit(invitation='TMLR/-/Submission',
            signatures=['~SomeFirstName_User1'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 13' },
                    'abstract': { 'value': 'Paper abstract' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight', 'Hugo Larochelle']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1', '~Hugo_Larochelle1']},
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    #'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'submission_length': { 'value': 'Regular submission (no more than 12 pages of main content)'}
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_13['id'])
        note_id_13=submission_note_13['note']['id']

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        assert openreview_client.get_invitation('TMLR/Paper13/Action_Editors/-/Recommendation')
        assert openreview_client.get_invitation(f"{venue_id}/Paper13/-/Official_Comment")

        editor_in_chief_group_id = f"{venue_id}/Editors_In_Chief"

        # Assign Action Editor and immediately remove  assignment
        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Joelle_Pineau1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_13,
            tail='~Joelle_Pineau1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ae_group = raia_client.get_group(f'{venue_id}/Paper13/Action_Editors')
        assert ae_group.members == ['~Joelle_Pineau1']

        ## Archive Joelle
        raia_client.remove_members_from_group(raia_client.get_group('TMLR/Action_Editors'), '~Joelle_Pineau1')
        raia_client.add_members_to_group(raia_client.get_group('TMLR/Action_Editors/Archived'), '~Joelle_Pineau1')

        joelle_paper13_anon_groups = joelle_client.get_groups(prefix=f'{venue_id}/Paper13/Action_Editor_.*', signatory='~Joelle_Pineau1')
        assert len(joelle_paper13_anon_groups) == 1
        joelle_paper13_anon_group = joelle_paper13_anon_groups[0]         

        ## Make a comment before approving the submission to be under review
        comment_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper13/-/Official_Comment',
            signatures=[joelle_paper13_anon_group.id],
            note=Note(
                signatures=[joelle_paper13_anon_group.id],
                readers=['TMLR/Editors_In_Chief', 'TMLR/Paper13/Action_Editors'],
                forum=note_id_13,
                replyto=note_id_13,
                content={
                    'comment': { 'value': 'I\'m not sure if I should accept this paper to be under review' }
                }
            )
        )
        
        ## Accept the submission 1
        under_review_note = joelle_client.post_note_edit(invitation= 'TMLR/Paper13/-/Review_Approval',
                                    signatures=[joelle_paper13_anon_group.id],
                                    note=Note(content={
                                        'under_review': { 'value': 'Appropriate for Review' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=under_review_note['id'])

        edits = openreview_client.get_note_edits(note_id_13, invitation='TMLR/-/Under_Review')
        helpers.await_queue_edit(openreview_client, edit_id=edits[0].id)

        helpers.await_queue_edit(openreview_client, invitation='TMLR/-/Under_Review')

        ## David Belanger
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper13/Action_Editors", '~David_Belanger1'],
            nonreaders=[f"{venue_id}/Paper13/Authors"],
            writers=[venue_id, f"{venue_id}/Paper13/Action_Editors"],
            signatures=[joelle_paper13_anon_group.id],
            head=note_id_13,
            tail='~David_Belanger1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ## Archive David
        david_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment_Availability',
            signatures=['~David_Belanger1'],
            head='TMLR/Reviewers',
            tail='~David_Belanger1',
            label='Unavailable'
        ))        
        #raia_client.remove_members_from_group(raia_client.get_group('TMLR/Reviewers'), '~David_Belanger1')
        #raia_client.add_members_to_group(raia_client.get_group('TMLR/Reviewers/Archived'), '~David_Belanger1')

        edit_group = raia_client.post_group_edit(
            invitation='TMLR/Reviewers/Archived/-/Member',
            signatures=['TMLR'],
            group=openreview.api.Group(
                members={
                    'add': ['~David_Belanger1']
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=edit_group['id'])        

        assert '~David_Belanger1' in openreview_client.get_group('TMLR/Reviewers/Archived').members
        assert '~David_Belanger1' not in openreview_client.get_group('TMLR/Reviewers').members
        assert openreview_client.get_edges_count(invitation='TMLR/Reviewers/-/Assignment_Availability', tail='~David_Belanger1') == 0
        assert openreview_client.get_edges_count(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~David_Belanger1') == 0
        assert openreview_client.get_edges_count(invitation='TMLR/Reviewers/-/Custom_Max_Papers', tail='~David_Belanger1') == 0

        # post a reviewer report about an archived reviewer TMLR/Reviewers/-/Reviewer_Report
        reviewer_report = raia_client.post_note_edit(invitation=f'{venue_id}/Reviewers/-/Reviewer_Report',
            signatures=['~Raia_Hadsell1'],
            note=Note(
                content={
                    'reviewer_id': { 'value': '~David_Belanger1' },
                    'report_reason': { 'value': ['Reviewer never submitted their review'] },
                    'comment': { 'value': 'This is a comment.' }
                }
            )
        )
        helpers.await_queue_edit(openreview_client, edit_id=reviewer_report['id'])

        ## Carlos Mondragon
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper13/Action_Editors", '~Carlos_Mondragon1'],
            nonreaders=[f"{venue_id}/Paper13/Authors"],
            writers=[venue_id, f"{venue_id}/Paper13/Action_Editors"],
            signatures=[joelle_paper13_anon_group.id],
            head=note_id_13,
            tail='~Carlos_Mondragon1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ## Javier Burroni
        paper_assignment_edge = joelle_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Assignment',
            readers=[venue_id, f"{venue_id}/Paper13/Action_Editors", '~Javier_Burroni1'],
            nonreaders=[f"{venue_id}/Paper13/Authors"],
            writers=[venue_id, f"{venue_id}/Paper13/Action_Editors"],
            signatures=[joelle_paper13_anon_group.id],
            head=note_id_13,
            tail='~Javier_Burroni1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        david_anon_groups=david_client.get_groups(prefix=f'{venue_id}/Paper13/Reviewer_.*', signatory='~David_Belanger1')
        assert len(david_anon_groups) == 1

        ## Post a review edit
        david_review_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper13/-/Review',
            signatures=[david_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=david_review_note['id'])

        assert openreview_client.get_edges_count(invitation='TMLR/Reviewers/-/Pending_Reviews', tail='~David_Belanger1') == 0

        carlos_anon_groups=carlos_client.get_groups(prefix=f'{venue_id}/Paper13/Reviewer_.*', signatory='~Carlos_Mondragon1')
        assert len(carlos_anon_groups) == 1

        ## Post a review edit
        carlos_review_note = carlos_client.post_note_edit(invitation=f'{venue_id}/Paper13/-/Review',
            signatures=[carlos_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=carlos_review_note['id'])

        javier_anon_groups=javier_client.get_groups(prefix=f'{venue_id}/Paper13/Reviewer_.*', signatory='~Javier_Burroni1')
        assert len(javier_anon_groups) == 1

        ## Post a review edit
        javier_review_note = javier_client.post_note_edit(invitation=f'{venue_id}/Paper13/-/Review',
            signatures=[javier_anon_groups[0].id],
            note=Note(
                content={
                    'summary_of_contributions': { 'value': 'summary_of_contributions' },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'claims_explanation' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'audience_explanation' },
                    'requested_changes': { 'value': 'requested_changes' },
                    'broader_impact_concerns': { 'value': 'broader_impact_concerns' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=javier_review_note['id'])                

        raia_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            readers=[venue_id],
            writers=[venue_id],
            signatures=[venue_id],
            invitation=openreview.api.Invitation(id=f'{venue_id}/Paper13/-/Official_Recommendation',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now()) + 1000,
                signatures=['TMLR/Editors_In_Chief']
            )
        )

        time.sleep(5) ## wait until the process function runs        

        ## Post a review recommendation
        official_recommendation_note = carlos_client.post_note_edit(invitation=f'{venue_id}/Paper13/-/Official_Recommendation',
            signatures=[carlos_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Accept' },
                    'certification_recommendations': { 'value': ['Featured Certification'] },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])        
        
        official_recommendation_note = david_client.post_note_edit(invitation=f'{venue_id}/Paper13/-/Official_Recommendation',
            signatures=[david_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Accept' },
                    'certification_recommendations': { 'value': ['Featured Certification', 'Reproducibility Certification'] },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        official_recommendation_note = javier_client.post_note_edit(invitation=f'{venue_id}/Paper13/-/Official_Recommendation',
            signatures=[javier_anon_groups[0].id],
            note=Note(
                content={
                    'decision_recommendation': { 'value': 'Accept' },
                    'certification_recommendations': { 'value': ['Featured Certification', 'Reproducibility Certification'] },
                    'claims_and_evidence': { 'value': 'Yes' },
                    'audience': { 'value': 'Yes' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=official_recommendation_note['id'])

        reviews = joelle_client.get_notes(forum=note_id_13, invitation=f'{venue_id}/Paper13/-/Review', sort= 'number:asc')

        for review in reviews:
            signature=review.signatures[0]
            rating_note=joelle_client.post_note_edit(invitation=f'{signature}/-/Rating',
                signatures=[joelle_paper13_anon_group.id],
                note=Note(
                    content={
                        'rating': { 'value': 'Exceeds expectations' }
                    }
                )
            )
            helpers.await_queue_edit(openreview_client, edit_id=rating_note['id'])
            process_logs = openreview_client.get_process_logs(id = rating_note['id'])
            assert len(process_logs) == 1
            assert process_logs[0]['status'] == 'ok'

        decision_note = joelle_client.post_note_edit(invitation=f'{venue_id}/Paper13/-/Decision',
            signatures=[joelle_paper13_anon_group.id],
            note=Note(
                content={
                    'claims_and_evidence': { 'value': 'Yes' },
                    'claims_explanation': { 'value': 'Accept' },
                    'audience': { 'value': 'Yes' },
                    'audience_explanation': { 'value': 'No' },
                    'recommendation': { 'value': 'Accept with minor revision' },
                    'additional_comments': { 'value': 'This is a good paper' },
                    'recommendation_to_iclr_track': { 'value': 'Strongly Recommend' },
                    'explain_recommendation_to_iclr_track': { 'value': 'I recommend this paper to be published in the ICLR track because...' }
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=decision_note['id'])

        approval_note = raia_client.post_note_edit(invitation='TMLR/Paper13/-/Decision_Approval',
            signatures=['TMLR/Editors_In_Chief'],
            note=Note(
            content= {
                'approval': { 'value': 'I approve the AE\'s decision.' },
                'comment_to_the_AE': { 'value': 'I agree with the AE' }
            }))

        helpers.await_queue_edit(openreview_client, edit_id=approval_note['id'])

        revision_note = test_client.post_note_edit(invitation=f'{venue_id}/Paper13/-/Camera_Ready_Revision',
            signatures=[f"{venue_id}/Paper13/Authors"],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 13 VERSION 2' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight', 'Hugo Larochelle']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1', '~Hugo_Larochelle1']},
                    'abstract': { 'value': 'Paper abstract' },
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'video': { 'value': 'https://youtube.com/dfenxkw'}
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=revision_note['id'])

        verification_note = joelle_client.post_note_edit(invitation='TMLR/Paper13/-/Camera_Ready_Verification',
                            signatures=[joelle_paper13_anon_group.id],
                            note=Note(
                                signatures=[joelle_paper13_anon_group.id],
                                content= {
                                    'verification': { 'value': 'I confirm that camera ready manuscript complies with the TMLR stylefile and, if appropriate, includes the minor revisions that were requested.' }
                                 }
                            ))

        helpers.await_queue_edit(openreview_client, edit_id=verification_note['id'])

        note = openreview_client.get_note(note_id_13)
        assert 'certifications' not in note.content
        assert note.content['_bibtex']['value'] == '''@article{
user''' + str(datetime.datetime.fromtimestamp(note.cdate/1000).year) + '''paper,
title={Paper title 13 {VERSION} 2},
author={SomeFirstName User and Melissa Eight and Hugo Larochelle},
journal={Transactions on Machine Learning Research},
issn={2835-8856},
year={''' + str(datetime.datetime.today().year) + '''},
url={https://openreview.net/forum?id=''' + note_id_13 + '''},
note={}
}'''        

        helpers.await_queue_edit(openreview_client, invitation='TMLR/-/Accepted', count=2)

        ## Edit submission as EIC
        revision_note = raia_client.post_note_edit(invitation=f'{venue_id}/Paper13/-/EIC_Revision',
            signatures=[f"{venue_id}/Editors_In_Chief"],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 13 VERSION 3' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight', 'Hugo Larochelle']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1', '~Hugo_Larochelle1']},
                    'abstract': { 'value': 'Paper abstract' },
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'video': { 'value': 'https://youtube.com/dfenxkw'}
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=revision_note['id'])        

        edit_group = raia_client.post_group_edit(
            invitation='TMLR/Expert_Reviewers/-/Member',
            signatures=['TMLR'],
            group=openreview.api.Group(
                members={
                    'add': ['~Hugo_Larochelle1']
                }
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id=edit_group['id'])

        assert openreview_client.get_group('TMLR/Expert_Reviewers').members == ['~Andrew_McCallumm1', '~Hugo_Larochelle1']

        note = openreview_client.get_note(note_id_13)
        assert note.content['certifications']['value'] == ['Expert Certification']
        assert note.content['_bibtex']['value'] == '''@article{
user''' + str(datetime.datetime.fromtimestamp(note.cdate/1000).year) + '''paper,
title={Paper title 13 {VERSION} 3},
author={SomeFirstName User and Melissa Eight and Hugo Larochelle},
journal={Transactions on Machine Learning Research},
issn={2835-8856},
year={''' + str(datetime.datetime.today().year) + '''},
url={https://openreview.net/forum?id=''' + note_id_13 + '''},
note={Expert Certification}
}'''
        assert note.content['expert_reviewers']['value'] == ['~Hugo_Larochelle1']                                                              

  
        note = openreview_client.get_note(note_id_13)
        journal.invitation_builder.expire_paper_invitations(note)

        ## Add Event certification
        raia_client.post_note_edit(invitation='TMLR/-/Event_Certification',
            signatures=["TMLR"],
            note=Note(
                id = note_id_13,
                content= {
                    'event_certifications': { 'value': ['lifelong-ml.cc/CoLLAs/2023/Journal_Track'] }
                }
            ))        

    def test_invite_external_reviewers(self, journal, openreview_client, test_client, helpers, selenium, request_page):

        venue_id = journal.venue_id
        test_client = OpenReviewClient(username='test@mail.com', password=helpers.strong_password)
        raia_client = OpenReviewClient(username='raia@mail.com', password=helpers.strong_password)
        samy_client = OpenReviewClient(username='samy@bengio.com', password=helpers.strong_password)


        ## Post the submission 14
        submission_note_14 = test_client.post_note_edit(invitation='TMLR/-/Submission',
            signatures=['~SomeFirstName_User1'],
            note=Note(
                content={
                    'title': { 'value': 'Paper title 14' },
                    'abstract': { 'value': 'Paper abstract' },
                    'authors': { 'value': ['SomeFirstName User', 'Melissa Eight', 'Hugo Larochelle']},
                    'authorids': { 'value': ['~SomeFirstName_User1', '~Melissa_Eight1', '~Hugo_Larochelle1']},
                    'pdf': {'value': '/pdf/' + 'p' * 40 +'.pdf' },
                    #'supplementary_material': { 'value': '/attachment/' + 's' * 40 +'.zip'},
                    'competing_interests': { 'value': 'None beyond the authors normal conflict of interests'},
                    'human_subjects_reporting': { 'value': 'Not applicable'},
                    'submission_length': { 'value': 'Regular submission (no more than 12 pages of main content)'}
                }
            ))

        helpers.await_queue_edit(openreview_client, edit_id=submission_note_14['id'])
        note_id_14=submission_note_14['note']['id']
        submission = openreview_client.get_note(note_id_14)

        Journal.update_affinity_scores(openreview.api.OpenReviewClient(username='openreview.net', password=helpers.strong_password), support_group_id='openreview.net/Support')

        assert openreview_client.get_invitation(f'TMLR/Paper{submission.number}/Action_Editors/-/Recommendation')
        assert openreview_client.get_invitation(f"{venue_id}/Paper{submission.number}/-/Official_Comment")

        editor_in_chief_group_id = f"{venue_id}/Editors_In_Chief"

        # Assign Action Editor and immediately remove  assignment
        paper_assignment_edge = raia_client.post_edge(openreview.api.Edge(invitation='TMLR/Action_Editors/-/Assignment',
            readers=[venue_id, editor_in_chief_group_id, '~Samy_Bengio1'],
            writers=[venue_id, editor_in_chief_group_id],
            signatures=[editor_in_chief_group_id],
            head=note_id_14,
            tail='~Samy_Bengio1',
            weight=1
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        ae_group = raia_client.get_group(f'{venue_id}/Paper{submission.number}/Action_Editors')
        assert ae_group.members == ['~Samy_Bengio1']

        joelle_paper13_anon_groups = samy_client.get_groups(prefix=f'{venue_id}/Paper{submission.number}/Action_Editor_.*', signatory='~Samy_Bengio1')
        assert len(joelle_paper13_anon_groups) == 1
        joelle_paper13_anon_group = joelle_paper13_anon_groups[0]         

        ## Accept the submission 1
        under_review_note = samy_client.post_note_edit(invitation= f'TMLR/Paper{submission.number}/-/Review_Approval',
                                    signatures=[joelle_paper13_anon_group.id],
                                    note=Note(content={
                                        'under_review': { 'value': 'Appropriate for Review' }
                                    }))

        helpers.await_queue_edit(openreview_client, edit_id=under_review_note['id'])

        edits = openreview_client.get_note_edits(note_id_14, invitation='TMLR/-/Under_Review')
        helpers.await_queue_edit(openreview_client, edit_id=edits[0].id)

        helpers.await_queue_edit(openreview_client, invitation='TMLR/-/Under_Review')

        ## Invite external reviewer with profile
        paper_assignment_edge = samy_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Invite_Assignment',
            signatures=[joelle_paper13_anon_group.id],
            head=note_id_14,
            tail='melisa@mailten.com',
            weight=1,
            label='Invitation Sent'
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        invite_edges=openreview_client.get_edges(invitation='TMLR/Reviewers/-/Invite_Assignment', head=note_id_14, tail='~Melisa_Bok1')
        assert len(invite_edges) == 1
        assert invite_edges[0].label == 'Invitation Sent'         

        messages = openreview_client.get_messages(to = 'melisa@mailten.com', subject = '[TMLR] Invitation to review paper titled "Paper title 14"')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Melisa Bok,\n\nYou were invited to review the paper number: {submission.number}, title: \"Paper title 14\".\n\nAbstract: Paper abstract\n\nPlease respond the invitation clicking the following link:\n\nhttps://openreview.net/invitation?id=TMLR/Reviewers/-/Assignment_Recruitment&user=~Melisa_Bok1&key=da9c8e30376e445b0d18011af6a8ca7863e5037e3f9aebc6aa4294e5aaa5c216&submission_id={submission.id}&inviter=~Samy_Bengio1\n\nThanks,\n\nTMLR Paper{submission.number} Action Editor {joelle_paper13_anon_group.id.split('_')[-1]}\nSamy Bengio\n\nPlease note that responding to this email will direct your reply to samy@bengio.com.\n'''

        messages = openreview_client.get_messages(to = 'samy@bengio.com', subject = '[TMLR] Invitation to review paper titled "Paper title 14"')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Samy Bengio,\n\nThe following invitation email was sent to Melisa Bok:\n\nHi Melisa Bok,\n\nYou were invited to review the paper number: {submission.number}, title: \"Paper title 14\".\n\nAbstract: Paper abstract\n\nPlease respond the invitation clicking the following link:\n\nhttps://openreview.net/invitation?id=TMLR/Reviewers/-/Assignment_Recruitment&user=~Melisa_Bok1&key=da9c8e30376e445b0d18011af6a8ca7863e5037e3f9aebc6aa4294e5aaa5c216&submission_id={submission.id}&inviter=~Samy_Bengio1\n\nThanks,\n\nTMLR Paper{submission.number} Action Editor {joelle_paper13_anon_group.id.split('_')[-1]}\nSamy Bengio\n\nPlease note that responding to this email will direct your reply to melisa@mailten.com.\n'''

        invitation_url = re.search('https://.*\n', messages[0]['content']['text']).group(0).replace('https://openreview.net', 'http://localhost:3030').replace('&amp;', '&')[:-1]
        helpers.respond_invitation(selenium, request_page, invitation_url, accept=True)

        helpers.await_queue_edit(openreview_client, invitation='TMLR/Reviewers/-/Assignment_Recruitment', count=1)

        invite_edges=openreview_client.get_edges(invitation='TMLR/Reviewers/-/Invite_Assignment', head=note_id_14, tail='~Melisa_Bok1')
        assert len(invite_edges) == 1
        assert invite_edges[0].label == 'Accepted'         

        assignment_edges=openreview_client.get_edges(invitation='TMLR/Reviewers/-/Assignment', head=note_id_14, tail='~Melisa_Bok1')
        assert len(assignment_edges) == 1

        helpers.await_queue_edit(openreview_client, edit_id=assignment_edges[0].id)

        messages = openreview_client.get_messages(to = 'melisa@mailten.com', subject = f'[TMLR] Reviewers Invitation accepted for paper {submission.number}: Paper title 14')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Melisa Bok,\nThank you for accepting the invitation to review the paper number: {submission.number}, title: Paper title 14.\n\nPlease go to the Tasks page and check your TMLR pending tasks: https://openreview.net/tasks\n\nIf you would like to change your decision, please follow the link in the previous invitation email and click on the \"Decline\" button.\n\nOpenReview Team\n\nPlease note that responding to this email will direct your reply to tmlr@jmlr.org.\n'''

        messages = openreview_client.get_messages(to = 'samy@bengio.com', subject = f'[TMLR] Reviewers Melisa Bok accepted to review paper {submission.number}: Paper title 14')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Samy Bengio,\nThe Reviewers Melisa Bok that you invited to review paper {submission.number} has accepted the invitation and is now assigned to the paper {submission.number}.\n\nOpenReview Team\n\nPlease note that responding to this email will direct your reply to tmlr@jmlr.org.\n'''

        messages = openreview_client.get_messages(to = 'melisa@mailten.com', subject = f'[TMLR] Assignment to review new TMLR submission {submission.number}: Paper title 14')
        assert len(messages) == 0

        messages = openreview_client.get_messages(to = 'melisa@mailten.com', subject = '[TMLR] Acknowledgement of Reviewer Responsibility')
        assert len(messages) == 0

        ## Invite external reviewer with no profile
        paper_assignment_edge = samy_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Invite_Assignment',
            signatures=[joelle_paper13_anon_group.id],
            head=note_id_14,
            tail='harold@hotmail.com',
            weight=1,
            label='Invitation Sent'
        ))        

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        messages = openreview_client.get_messages(to = 'harold@hotmail.com', subject = '[TMLR] Invitation to review paper titled "Paper title 14"')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi harold@hotmail.com,\n\nYou were invited to review the paper number: {submission.number}, title: \"Paper title 14\".\n\nAbstract: Paper abstract\n\nPlease respond the invitation clicking the following link:\n\nhttps://openreview.net/invitation?id=TMLR/Reviewers/-/Assignment_Recruitment&user=harold@hotmail.com&key=5702b25b819d98308e99b9784e37d7327e511efbd618e44df194ccefc6dcc96c&submission_id={submission.id}&inviter=~Samy_Bengio1\n\nThanks,\n\nTMLR Paper{submission.number} Action Editor {joelle_paper13_anon_group.id.split('_')[-1]}\nSamy Bengio\n\nPlease note that responding to this email will direct your reply to samy@bengio.com.\n'''

        invitation_url = re.search('https://.*\n', messages[0]['content']['text']).group(0).replace('https://openreview.net', 'http://localhost:3030').replace('&amp;', '&')[:-1]
        helpers.respond_invitation(selenium, request_page, invitation_url, accept=True)

        helpers.await_queue_edit(openreview_client, invitation='TMLR/Reviewers/-/Assignment_Recruitment', count=2)

        invite_edges=openreview_client.get_edges(invitation='TMLR/Reviewers/-/Invite_Assignment', head=note_id_14, tail='harold@hotmail.com')
        assert len(invite_edges) == 1
        assert invite_edges[0].label == 'Pending Sign Up'         

        assignment_edges=openreview_client.get_edges(invitation='TMLR/Reviewers/-/Assignment', head=note_id_14, tail='harold@hotmail.com')
        assert len(assignment_edges) == 0

        messages = openreview_client.get_messages(to = 'harold@hotmail.com', subject = f'[TMLR] Reviewers Invitation accepted for paper {submission.number}: Paper title 14, assignment pending')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi harold@hotmail.com,\nThank you for accepting the invitation to review the paper number: {submission.number}, title: Paper title 14.\n\nPlease signup in OpenReview using the email address harold@hotmail.com and complete your profile.\nConfirmation of the assignment is pending until your profile is active and no conflicts of interest are detected.\n\nIf you would like to change your decision, please follow the link in the previous invitation email and click on the \"Decline\" button.\n\nOpenReview Team\n\nPlease note that responding to this email will direct your reply to tmlr@jmlr.org.\n'''

        messages = openreview_client.get_messages(to = 'samy@bengio.com', subject = f'[TMLR] Reviewers harold@hotmail.com accepted to review paper {submission.number}: Paper title 14, assignment pending')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Samy Bengio,\nThe Reviewers harold@hotmail.com that you invited to review paper {submission.number} has accepted the invitation.\n\nConfirmation of the assignment is pending until the invited reviewer creates a profile in OpenReview and no conflicts of interest are detected.\n\nOpenReview Team\n\nPlease note that responding to this email will direct your reply to tmlr@jmlr.org.\n'''

        ## Invite external reviewer with a conflict of interest
        with pytest.raises(openreview.OpenReviewException, match=r'Conflict detected for harold@mail'):
            paper_assignment_edge = samy_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Invite_Assignment',
                signatures=[joelle_paper13_anon_group.id],
                head=note_id_14,
                tail='harold@mail.com',
                weight=1,
                label='Invitation Sent'
            ))

        ## Invite reviewer that is already in the pool
        with pytest.raises(openreview.OpenReviewException, match=r'tail "javier@mailtwo.com" is member of TMLR/Reviewers'):
            paper_assignment_edge = samy_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Invite_Assignment',
                signatures=[joelle_paper13_anon_group.id],
                head=note_id_14,
                tail='javier@mailtwo.com',
                weight=1,
                label='Invitation Sent'
            ))

        ## Invite reviewer that is already has an assignment
        with pytest.raises(openreview.OpenReviewException, match=r'Already invited as ~Melisa_Bok1'):
            paper_assignment_edge = samy_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Invite_Assignment',
                signatures=[joelle_paper13_anon_group.id],
                head=note_id_14,
                tail='melisa@mailten.com',
                weight=1,
                label='Invitation Sent'
            ))

        ## Run Job
        openreview.journal.Journal.check_new_profiles(openreview_client, support_group_id = 'openreview.net/Support')                        

        invite_edges=openreview_client.get_edges(invitation='TMLR/Reviewers/-/Invite_Assignment', head=note_id_14, tail='harold@hotmail.com')
        assert len(invite_edges) == 1
        assert invite_edges[0].label == 'Pending Sign Up'

        helpers.create_user('harold@hotmail.com', 'Harold', 'Red')

        ## Run Job
        openreview.journal.Journal.check_new_profiles(openreview_client, support_group_id = 'openreview.net/Support')                        

        invite_edges=openreview_client.get_edges(invitation='TMLR/Reviewers/-/Invite_Assignment', head=note_id_14, tail='harold@hotmail.com')
        assert len(invite_edges) == 0
        invite_edges=openreview_client.get_edges(invitation='TMLR/Reviewers/-/Invite_Assignment', head=note_id_14, tail='~Harold_Red1')
        assert len(invite_edges) == 1
        assert invite_edges[0].label == 'Accepted'

        messages = openreview_client.get_messages(to = 'harold@hotmail.com', subject = f'[TMLR] Reviewer Assignment confirmed for paper {submission.number}: Paper title 14')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Harold Red,\nThank you for accepting the invitation to review the paper number: {submission.number}, title: Paper title 14.\n\nPlease go to the Tasks page and check your TMLR pending tasks: https://openreview.net/tasks\n\nIf you would like to change your decision, please click the Decline link in the previous invitation email.\n\nOpenReview Team\n\nPlease note that responding to this email will direct your reply to tmlr@jmlr.org.\n'''

        messages = openreview_client.get_messages(to = 'samy@bengio.com', subject = f'[TMLR] Reviewer Harold Red signed up and is assigned to paper {submission.number}: Paper title 14')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi Samy Bengio,\nThe Reviewer Harold Red that you invited to review paper {submission.number} has accepted the invitation, signed up and is now assigned to the paper {submission.number}.\n\nOpenReview Team\n\nPlease note that responding to this email will direct your reply to tmlr@jmlr.org.\n'''

        assignment_edges=openreview_client.get_edges(invitation='TMLR/Reviewers/-/Assignment', head=note_id_14, tail='~Harold_Red1')
        helpers.await_queue_edit(openreview_client, edit_id=assignment_edges[0].id)

        ## Invite archived reviewers with status unavailable
        paper_assignment_edge = samy_client.post_edge(openreview.api.Edge(invitation='TMLR/Reviewers/-/Invite_Assignment',
            signatures=[joelle_paper13_anon_group.id],
            head=note_id_14,
            tail='~David_Belanger1',
            weight=1,
            label='Invitation Sent'
        ))

        helpers.await_queue_edit(openreview_client, edit_id=paper_assignment_edge.id)

        invite_edges=openreview_client.get_edges(invitation='TMLR/Reviewers/-/Invite_Assignment', head=note_id_14, tail='~David_Belanger1')
        assert len(invite_edges) == 1
        assert invite_edges[0].label == 'Invitation Sent'         

        messages = openreview_client.get_messages(to = 'david@mailone.com', subject = '[TMLR] Invitation to review paper titled "Paper title 14"')
        assert len(messages) == 1
        assert messages[0]['content']['text'] == f'''Hi David Belanger,\n\nYou were invited to review the paper number: {submission.number}, title: \"Paper title 14\".\n\nAbstract: Paper abstract\n\nPlease respond the invitation clicking the following link:\n\nhttps://openreview.net/invitation?id=TMLR/Reviewers/-/Assignment_Recruitment&user=~David_Belanger1&key=1fb0276b3b49168f226d7d72a35ce85c60ad895f83a0e767b1a0c42a3fd9fd16&submission_id={submission.id}&inviter=~Samy_Bengio1\n\nThanks,\n\nTMLR Paper{submission.number} Action Editor {joelle_paper13_anon_group.id.split('_')[-1]}\nSamy Bengio\n\nPlease note that responding to this email will direct your reply to samy@bengio.com.\n'''

        invitation_url = re.search('https://.*\n', messages[0]['content']['text']).group(0).replace('https://openreview.net', 'http://localhost:3030').replace('&amp;', '&')[:-1]
        helpers.respond_invitation(selenium, request_page, invitation_url, accept=True)

        helpers.await_queue_edit(openreview_client, invitation='TMLR/Reviewers/-/Assignment_Recruitment', count=3)

        invite_edges=openreview_client.get_edges(invitation='TMLR/Reviewers/-/Invite_Assignment', head=note_id_14, tail='~David_Belanger1')
        assert len(invite_edges) == 1
        assert invite_edges[0].label == 'Accepted'         

        assignment_edges=openreview_client.get_edges(invitation='TMLR/Reviewers/-/Assignment', head=note_id_14, tail='~David_Belanger1')
        assert len(assignment_edges) == 1

        helpers.await_queue_edit(openreview_client, edit_id=assignment_edges[0].id)

        ## compute preferred emails
        openreview_client.post_invitation_edit(
            invitations='TMLR/-/Edit',
            signatures=['~Super_User1'],
            invitation=openreview.api.Invitation(
                id='TMLR/-/Preferred_Emails',
                cdate=openreview.tools.datetime_millis(datetime.datetime.now()) + 2000,
            )
        )

        helpers.await_queue_edit(openreview_client, edit_id='TMLR/-/Preferred_Emails-0-0', count=3)

        ## Check preferred emails
        assert openreview_client.get_edges_count(invitation='TMLR/-/Preferred_Emails') == 17        
        
        note = openreview_client.get_note(note_id_14)
        journal.invitation_builder.expire_paper_invitations(note)
        journal.invitation_builder.expire_reviewer_responsibility_invitations()
        journal.invitation_builder.expire_assignment_availability_invitations()        
