from datetime import datetime, timedelta, timezone
import pandas as pd

def calculate_commit_metrics(commits):
    if not commits:
        return 0, None
    commit_dates = [c["commit"]["author"]["date"] for c in commits]
    df = pd.DataFrame(commit_dates, columns=["date"])
    df["date"] = pd.to_datetime(df["date"])

    now = datetime.now(tz=timezone.utc)
    last_commit_date = df["date"].max()
    days_since_last_commit = (now - last_commit_date).days

    commits_last_30_days = df[df["date"] >= now - timedelta(days=30)].shape[0]

    return commits_last_30_days, days_since_last_commit

def calculate_issue_metrics(issues):
    if not issues:
        return 0

    total_issues = 0
    closed_issues = 0

    for issue in issues:
        if "pull_request" in issue:
            continue
        total_issues += 1
        if issue["state"] == "closed":
            closed_issues += 1

    if total_issues == 0:
        return 0

    return round((closed_issues / total_issues) * 100, 2)

def calculate_health_score(commits_last_30, days_since_last_commit, issue_closure_rate):
    score = 0

    score += min(commits_last_30, 40)

    if days_since_last_commit is not None:
        if days_since_last_commit <= 7:
            score += 30
        elif days_since_last_commit <= 30:
            score += 20
        elif days_since_last_commit <= 90:
            score += 10

    score += (issue_closure_rate / 100) * 30

    return round(score, 2)