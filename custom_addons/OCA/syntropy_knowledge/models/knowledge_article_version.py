# Copyright 2026 Syntropy
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class KnowledgeArticleVersion(models.Model):
    """Historial de versiones de un artículo de conocimiento."""

    _name = "knowledge.article.version"
    _description = "Knowledge Article Version"
    _order = "version_number desc"
    _rec_name = "display_name_computed"

    name = fields.Char(
        string="Nombre de versión",
        required=True,
    )
    display_name_computed = fields.Char(
        string="Nombre",
        compute="_compute_display_name_computed",
        store=True,
    )
    article_id = fields.Many2one(
        comodel_name="knowledge.article",
        string="Artículo",
        required=True,
        ondelete="cascade",
        index=True,
    )
    content = fields.Html(
        string="Contenido",
        readonly=True,
        sanitize=False,
    )
    summary = fields.Text(
        string="Resumen",
        readonly=True,
    )
    version_number = fields.Integer(
        string="Nº Versión",
        required=True,
        readonly=True,
    )
    author_id = fields.Many2one(
        comodel_name="res.users",
        string="Autor de la versión",
        required=True,
        readonly=True,
    )
    create_date = fields.Datetime(
        string="Fecha de creación",
        readonly=True,
    )

    def _compute_display_name_computed(self):
        for version in self:
            version.display_name_computed = (
                f"{version.article_id.name} - {version.name}"
            )

    def action_restore_version(self):
        """Restaurar esta versión como contenido actual del artículo."""
        self.ensure_one()
        self.article_id.write(
            {
                "content": self.content,
                "summary": self.summary,
            }
        )
        self.article_id.message_post(
            body=f"Contenido restaurado desde la versión {self.name}.",
            message_type="comment",
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": "knowledge.article",
            "res_id": self.article_id.id,
            "view_mode": "form",
            "target": "current",
        }
