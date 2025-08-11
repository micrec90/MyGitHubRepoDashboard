import streamlit as st
import pandas as pd
import plotly.express as px

from api import fetch_repo_data, fetch_issues, fetch_commits
from metrics import calculate_commit_metrics, calculate_issue_metrics, calculate_health_score

st.title("📊 GitHub Repo Health Dashboard")
repo_input = st.text_input("Enter repo (owner/name)", placeholder="<user>/<repo>")
token = st.text_input("GitHub Personal Access Token (optional)", type="password")

if st.button("Fetch data"):
    try:
        owner, repo = repo_input.split("/")
        repo_data = fetch_repo_data(owner, repo, token)
        issues = fetch_issues(owner, repo, token=token)
        commits = fetch_commits(owner, repo, token=token)

        commits_last_30, days_since_last_commit = calculate_commit_metrics(commits)
        issue_closure_rate = calculate_issue_metrics(issues)
        health_score = calculate_health_score(commits_last_30, days_since_last_commit, issue_closure_rate)

        st.subheader("Overview")
        st.write(f"**Description:** {repo_data.get('description')}")
        st.write(f"⭐ Stars: {repo_data.get('stargazers_count')}")
        st.write(f"🍴 Forks: {repo_data.get('forks_count')}")
        st.write(f"👀 Watchers: {repo_data.get('watchers_count')}")
        st.write(f"📅 Last Updated: {repo_data.get('updated_at')}")

        st.subheader("📈 Health Metrics")
        st.write(f"Commits (last 30 days): {commits_last_30}")
        st.write(f"Days since last commit: {days_since_last_commit}")
        st.write(f"Issue closure rate: {issue_closure_rate}%")
        st.write(f"💡 Health Score: **{health_score} / 100**")

        commit_dates = [c["commit"]["author"]["date"] for c in commits]
        df_commits = pd.DataFrame(commit_dates, columns=["date"])
        df_commits["date"] = pd.to_datetime(df_commits["date"])
        commits_per_day = df_commits.groupby(df_commits["date"].dt.date).size().reset_index(name="count")
        fig = px.bar(commits_per_day, x="date", y="count", title="Commit Activity")
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error: {e}")