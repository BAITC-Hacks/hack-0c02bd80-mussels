import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from config import DATA_DIR
from services.seed_data import (
    get_initial_drafts,
    get_initial_tasks,
    get_initial_teams,
    get_initial_proposals,
    get_initial_milestones
)

class Storage:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.tasks_file = self.data_dir / "tasks.json"
        self.drafts_file = self.data_dir / "drafts.json"
        self.teams_file = self.data_dir / "teams.json"
        self.proposals_file = self.data_dir / "proposals.json"
        self.milestones_file = self.data_dir / "milestones.json"
        self.ensure_initialized()

    def ensure_initialized(self) -> None:
        if not self.tasks_file.exists():
            self.save_tasks(get_initial_tasks())
        if not self.drafts_file.exists():
            self.save_drafts(get_initial_drafts())
        if not self.teams_file.exists():
            self.save_teams(get_initial_teams())
        if not self.proposals_file.exists():
            self.save_proposals(get_initial_proposals())
        if not self.milestones_file.exists():
            self.save_milestones(get_initial_milestones())

    def reset_all_data(self) -> None:
        self.save_tasks(get_initial_tasks())
        self.save_drafts(get_initial_drafts())
        self.save_teams(get_initial_teams())
        self.save_proposals(get_initial_proposals())
        self.save_milestones(get_initial_milestones())

    def _read_json(self, path: Path) -> List[Dict[str, Any]]:
        try:
            if not path.exists():
                return []
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _write_json(self, path: Path, data: List[Dict[str, Any]]) -> None:
        temp_path = path.with_suffix(".tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        temp_path.replace(path)

    # Tasks
    def load_tasks(self) -> List[Dict[str, Any]]:
        tasks = self._read_json(self.tasks_file)
        # Sort by rating descending as required by catalog rules
        tasks.sort(key=lambda t: t.get("rating", 0), reverse=True)
        return tasks

    def save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        self._write_json(self.tasks_file, tasks)

    def get_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        for task in self.load_tasks():
            if task.get("id") == task_id:
                return task
        return None

    def upsert_task(self, task_data: Dict[str, Any]) -> None:
        tasks = self.load_tasks()
        existing_idx = next((i for i, t in enumerate(tasks) if t["id"] == task_data["id"]), None)
        if existing_idx is not None:
            tasks[existing_idx] = task_data
        else:
            tasks.append(task_data)
        self.save_tasks(tasks)

    # Drafts
    def load_drafts(self) -> List[Dict[str, Any]]:
        return self._read_json(self.drafts_file)

    def save_drafts(self, drafts: List[Dict[str, Any]]) -> None:
        self._write_json(self.drafts_file, drafts)

    def add_draft(self, draft: Dict[str, Any]) -> None:
        drafts = self.load_drafts()
        drafts.append(draft)
        self.save_drafts(drafts)

    # Teams
    def load_teams(self) -> List[Dict[str, Any]]:
        return self._read_json(self.teams_file)

    def save_teams(self, teams: List[Dict[str, Any]]) -> None:
        self._write_json(self.teams_file, teams)

    def get_team_by_id(self, team_id: str) -> Optional[Dict[str, Any]]:
        for team in self.load_teams():
            if team.get("id") == team_id:
                return team
        return None

    def add_team_points(self, team_id: str, points: int) -> None:
        teams = self.load_teams()
        for team in teams:
            if team.get("id") == team_id:
                team["progress_points"] = team.get("progress_points", 0) + points
                break
        self.save_teams(teams)

    # Proposals
    def load_proposals(self) -> List[Dict[str, Any]]:
        return self._read_json(self.proposals_file)

    def save_proposals(self, proposals: List[Dict[str, Any]]) -> None:
        self._write_json(self.proposals_file, proposals)

    def get_proposals_for_task(self, task_id: str) -> List[Dict[str, Any]]:
        return [p for p in self.load_proposals() if p.get("task_id") == task_id]

    def add_proposal(self, proposal: Dict[str, Any]) -> None:
        proposals = self.load_proposals()
        proposals.append(proposal)
        self.save_proposals(proposals)

    def update_proposal_status(self, proposal_id: str, status: str, comment: str = "") -> Optional[Dict[str, Any]]:
        proposals = self.load_proposals()
        updated = None
        for p in proposals:
            if p.get("id") == proposal_id:
                p["status"] = status
                if comment:
                    p["review_comment"] = comment
                updated = p
                break
        if updated:
            self.save_proposals(proposals)
        return updated

    # Milestones
    def load_milestones(self) -> List[Dict[str, Any]]:
        return self._read_json(self.milestones_file)

    def save_milestones(self, milestones: List[Dict[str, Any]]) -> None:
        self._write_json(self.milestones_file, milestones)

    def get_milestones_for_task_team(self, task_id: str, team_id: str) -> List[Dict[str, Any]]:
        return [
            m for m in self.load_milestones()
            if m.get("task_id") == task_id and m.get("team_id") == team_id
        ]

    def add_milestone(self, milestone: Dict[str, Any]) -> None:
        milestones = self.load_milestones()
        milestones.append(milestone)
        self.save_milestones(milestones)

    def complete_milestone(self, milestone_id: str) -> Optional[Dict[str, Any]]:
        from datetime import datetime
        milestones = self.load_milestones()
        target = None
        for m in milestones:
            if m.get("id") == milestone_id and m.get("status") != "completed":
                m["status"] = "completed"
                m["completed_at"] = datetime.now().isoformat()
                target = m
                break
        if target:
            self.save_milestones(milestones)
            teams = self.load_teams()
            for team in teams:
                if team.get("id") == target.get("team_id"):
                    team["progress_points"] = team.get("progress_points", 0) + target.get("points", 25)
                    cm = team.get("completed_milestones", [])
                    if target["id"] not in cm:
                        cm.append(target["id"])
                    team["completed_milestones"] = cm
                    break
            self.save_teams(teams)
        return target

