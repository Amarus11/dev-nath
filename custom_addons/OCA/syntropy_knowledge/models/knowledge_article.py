# Copyright 2026 Syntropy
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class KnowledgeArticle(models.Model):
    """Artículo de conocimiento con versionado, etiquetas y favoritos."""

    _name = "knowledge.article"
    _description = "Knowledge Article"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, write_date desc"

    # ── Campos principales ───────────────────────────────────────────
    name = fields.Char(
        string="Título",
        required=True,
        tracking=True,
        translate=True,
    )
    summary = fields.Text(
        string="Resumen",
        help="Breve descripción del contenido del artículo",
        translate=True,
    )
    content = fields.Html(
        string="Contenido",
        sanitize=False,
        help="Contenido completo del artículo en formato HTML",
    )
    sequence = fields.Integer(
        string="Secuencia",
        default=10,
    )
    active = fields.Boolean(
        string="Activo",
        default=True,
        tracking=True,
    )

    # ── Clasificación ────────────────────────────────────────────────
    category_id = fields.Many2one(
        comodel_name="knowledge.category",
        string="Categoría",
        required=True,
        tracking=True,
        index=True,
        ondelete="restrict",
    )
    tag_ids = fields.Many2many(
        comodel_name="knowledge.tag",
        relation="knowledge_article_tag_rel",
        column1="article_id",
        column2="tag_id",
        string="Etiquetas",
    )

    # ── Estado y flujo ───────────────────────────────────────────────
    state = fields.Selection(
        selection=[
            ("draft", "Borrador"),
            ("review", "En revisión"),
            ("published", "Publicado"),
            ("archived", "Archivado"),
        ],
        string="Estado",
        default="draft",
        required=True,
        tracking=True,
        index=True,
        copy=False,
    )
    priority = fields.Selection(
        selection=[
            ("0", "Normal"),
            ("1", "Importante"),
            ("2", "Urgente"),
        ],
        string="Prioridad",
        default="0",
    )

    # ── Autoría y fechas ─────────────────────────────────────────────
    author_id = fields.Many2one(
        comodel_name="res.users",
        string="Autor",
        default=lambda self: self.env.user,
        required=True,
        tracking=True,
        index=True,
    )
    reviewer_id = fields.Many2one(
        comodel_name="res.users",
        string="Revisor",
        tracking=True,
    )
    publish_date = fields.Datetime(
        string="Fecha de publicación",
        readonly=True,
        copy=False,
    )
    last_review_date = fields.Datetime(
        string="Última revisión",
        readonly=True,
        copy=False,
    )

    # ── Versionado ───────────────────────────────────────────────────
    version_ids = fields.One2many(
        comodel_name="knowledge.article.version",
        inverse_name="article_id",
        string="Historial de versiones",
        readonly=True,
    )
    version_count = fields.Integer(
        string="Nº Versiones",
        compute="_compute_version_count",
    )
    current_version = fields.Integer(
        string="Versión actual",
        default=1,
        readonly=True,
        copy=False,
    )

    # ── Favoritos ────────────────────────────────────────────────────
    favorite_ids = fields.One2many(
        comodel_name="knowledge.favorite",
        inverse_name="article_id",
        string="Favoritos",
    )
    favorite_count = fields.Integer(
        string="Favoritos",
        compute="_compute_favorite_count",
    )
    is_favorite = fields.Boolean(
        string="Es favorito",
        compute="_compute_is_favorite",
        inverse="_inverse_is_favorite",
    )

    # ── Métricas ─────────────────────────────────────────────────────
    view_count = fields.Integer(
        string="Vistas",
        default=0,
        readonly=True,
        copy=False,
    )

    # ── Imagen e identidad visual ────────────────────────────────────
    cover_image = fields.Binary(
        string="Imagen de portada",
        attachment=True,
    )
    icon = fields.Char(
        string="Icono",
        default="📄",
    )
    color = fields.Integer(
        string="Color",
        default=0,
    )

    # ── Compañía ─────────────────────────────────────────────────────
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Compañía",
        default=lambda self: self.env.company,
        index=True,
    )

    # ── Campos computados relacionales ───────────────────────────────
    parent_category_id = fields.Many2one(
        related="category_id.parent_id",
        string="Categoría padre",
        store=True,
        readonly=True,
    )

    # ══════════════════════════════════════════════════════════════════
    # Métodos computados
    # ══════════════════════════════════════════════════════════════════

    def _compute_version_count(self):
        for article in self:
            article.version_count = len(article.version_ids)

    def _compute_favorite_count(self):
        for article in self:
            article.favorite_count = len(article.favorite_ids)

    def _compute_is_favorite(self):
        for article in self:
            article.is_favorite = bool(
                article.favorite_ids.filtered(
                    lambda f: f.user_id == self.env.user
                )
            )

    def _inverse_is_favorite(self):
        Favorite = self.env["knowledge.favorite"]
        for article in self:
            existing = Favorite.search(
                [
                    ("article_id", "=", article.id),
                    ("user_id", "=", self.env.uid),
                ],
                limit=1,
            )
            if article.is_favorite and not existing:
                Favorite.create(
                    {
                        "article_id": article.id,
                        "user_id": self.env.uid,
                    }
                )
            elif not article.is_favorite and existing:
                existing.unlink()

    # ══════════════════════════════════════════════════════════════════
    # Acciones de flujo de trabajo
    # ══════════════════════════════════════════════════════════════════

    def action_draft(self):
        """Regresar a borrador."""
        self.write({"state": "draft"})

    def action_review(self):
        """Enviar a revisión."""
        self.write({"state": "review"})

    def action_publish(self):
        """Publicar artículo y crear versión."""
        for article in self:
            article._create_version()
        self.write(
            {
                "state": "published",
                "publish_date": fields.Datetime.now(),
            }
        )

    def action_archive_article(self):
        """Archivar artículo."""
        self.write({"state": "archived", "active": False})

    def action_unarchive_article(self):
        """Des-archivar artículo."""
        self.write({"state": "draft", "active": True})

    # ══════════════════════════════════════════════════════════════════
    # Versionado
    # ══════════════════════════════════════════════════════════════════

    def _create_version(self):
        """Crea un snapshot del contenido actual como nueva versión."""
        self.ensure_one()
        self.current_version += 1
        self.env["knowledge.article.version"].create(
            {
                "article_id": self.id,
                "name": f"v{self.current_version}",
                "content": self.content,
                "summary": self.summary,
                "version_number": self.current_version,
                "author_id": self.env.uid,
            }
        )

    def action_view_versions(self):
        """Abrir historial de versiones del artículo."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": f"Versiones: {self.name}",
            "res_model": "knowledge.article.version",
            "view_mode": "list,form",
            "domain": [("article_id", "=", self.id)],
            "context": {"default_article_id": self.id},
        }

    # ══════════════════════════════════════════════════════════════════
    # Métricas
    # ══════════════════════════════════════════════════════════════════

    def action_increment_view(self):
        """Incrementar contador de vistas (llamado al abrir el artículo)."""
        for article in self:
            article.sudo().write({"view_count": article.view_count + 1})

    @api.model
    def read(self, fields=None, load="_classic_read"):
        """Override para incrementar vistas al leer un artículo."""
        result = super().read(fields=fields, load=load)
        return result
