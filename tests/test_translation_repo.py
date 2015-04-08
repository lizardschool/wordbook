from wordbook.domain.repo.translation import Repo
from wordbook.domain.models import Translation


def test_add_translation():
    print("JOJOOJOJJOJOJOJ")
    repo = Repo()
    repo.add_translation(
        Translation(from_language='en', to_language='pl', word='Apple', ipa='apple', translated='Jabłko')
    )
