
class DBLoadError(Exception):
    def __init__(self, line_no, stmt):
        self.line_no = line_no
        self.stmt_head = stmt[:16] + ' ...' if len(stmt) > 16 else stmt

    def __str__(self):
        return f"Error loading DB: {self.line_no}: {self.stmt_head}"
