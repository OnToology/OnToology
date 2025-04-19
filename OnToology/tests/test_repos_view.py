import unittest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from OnToology.views import repos_view


class ReposViewTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = MagicMock()
        self.user.is_authenticated = True
        self.repo_url = 'http://github.com/user/repo'

    @patch('OnToology.views.render')
    def test_repos_view_without_repo_param(self, mock_render):
        request = self.factory.get('/repos')
        request.user = self.user
        self.user.repos.all.return_value = ['repo1', 'repo2']

        repos_view(request)

        mock_render.assert_called_once_with(request, 'repos.html', {'repos': ['repo1', 'repo2']})

    @patch('OnToology.views.render')
    def test_repos_view_repo_not_belonging_to_user(self, mock_render):
        request = self.factory.get('/repos?repo=' + self.repo_url)
        request.user = self.user
        self.user.repos.filter.return_value = []

        repos_view(request)

        mock_render.assert_called_once_with(
            request,
            'msg.html',
            {'msg': 'This repo does not belong to your user account.'}
        )

    @patch('OnToology.views.get_pub_page', return_value='https://pages.github.io/repo')
    @patch('OnToology.views.get_repo_branches', return_value=['main', 'gh-pages'])
    @patch('OnToology.views.render')
    def test_repos_view_valid_repo_with_branch(self, mock_render, mock_get_branches, mock_get_pub):
        request = self.factory.get(f'/repos?repo={self.repo_url}&branch=main')
        request.user = self.user
        mock_repo = MagicMock()
        self.user.repos.filter.return_value = [mock_repo]

        repos_view(request)

        mock_render.assert_called_once_with(
            request,
            'repo.html',
            {
                'repo': mock_repo,
                'branch': 'main',
                'branches': ['main'],
                'pub_url': 'https://pages.github.io/repo'
            }
        )

    @patch('OnToology.views.get_pub_page', return_value='')
    @patch('OnToology.views.get_repo_branches', return_value=['main', 'gh-pages'])
    @patch('OnToology.views.render')
    def test_repos_view_valid_repo_without_branch(self, mock_render, mock_get_branches, mock_get_pub):
        request = self.factory.get(f'/repos?repo={self.repo_url}')
        request.user = self.user
        mock_repo = MagicMock()
        self.user.repos.filter.return_value = [mock_repo]

        repos_view(request)

        mock_render.assert_called_once_with(
            request,
            'repo.html',
            {
                'repo': mock_repo,
                'branch': 'main',
                'branches': ['main'],
                'pub_url': ''
            }
        )

    @patch('OnToology.views.render')
    @patch('OnToology.views.get_repo_branches', side_effect=Exception("GitHub error"))
    def test_repos_view_get_branches_exception(self, mock_get_branches, mock_render):
        request = self.factory.get(f'/repos?repo={self.repo_url}')
        request.user = self.user
        self.user.repos.filter.return_value = [MagicMock()]

        repos_view(request)

        mock_render.assert_called_once_with(
            request,
            'msg.html',
            {'msg': 'Error getting repository branches from GitHub.'}
        )


if __name__ == '__main__':
    unittest.main()
