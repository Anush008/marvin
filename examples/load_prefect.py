from marvin.bots import Bot
from marvin.loaders.base import MultiLoader
from marvin.loaders.discourse import DiscourseLoader
from marvin.loaders.github import GitHubIssueLoader, GitHubRepoLoader
from marvin.loaders.web import SitemapLoader
from marvin.plugins.chroma import SimpleChromaSearch
from marvin.plugins.duckduckgo import DuckDuckGo


async def load_prefect_things():
    prefect_docs = SitemapLoader(  # gimme da docs
        urls=["https://docs.prefect.io/sitemap.xml"],
        exclude=["api-ref"],
    )

    GitHubIssueLoader(  # gimme da issues
        repo="prefecthq/prefect",
        n_issues=50,
    )

    GitHubRepoLoader(  # gimme da source
        repo="prefecthq/prefect", glob="**/*.py", exclude_glob="**/tests/**"
    )

    DiscourseLoader(  # gimme da discourse
        url="https://discourse.prefect.io",
    )

    GitHubRepoLoader(  # gimme da recipes
        repo="prefecthq/prefect-recipes",
        glob="**/*.py",
        exclude_glob="prefect-v1-legacy/**",
    )

    prefect_loader = MultiLoader(
        loaders=[
            prefect_docs,
            # prefect_discourse,
            # prefect_github_issues,
            # prefect_recipes,
            # prefect_source_code,
        ]
    )
    await prefect_loader.load_and_store()


async def hello_marvin():
    # await load_prefect_things()
    bot = Bot(
        name="marvin",
        personality="like the robot from HHGTTG, depressed but helpful",
        instructions=(
            "Use the `SimpleChromaSearch` plugin to retrieve context"
            " when a user asks a question, or requests information"
            " about cloud computing as it relates to Prefect."
            " For current events, use the `DuckDuckGo` plugin."
        ),
        plugins=[
            SimpleChromaSearch(
                keywords=[
                    "prefect",
                    "block",
                    "flow",
                    "task",
                    "deployment",
                    "work pool",
                    "cloud",
                ]
            ),
            DuckDuckGo(),
        ],
    )
    await bot.interactive_chat()

    print(await bot.history.to_jsonl())


if __name__ == "__main__":
    import asyncio

    import marvin

    marvin.settings.log_level = "DEBUG"
    # marvin.settings.openai_model_name = "gpt-4"
    asyncio.run(hello_marvin())
