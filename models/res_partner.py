from datetime import date, timedelta

from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'
    _description = 'Partner_Inherit'
    _order = 'last_trx_date asc'

    last_trx_date_auto = fields.Date(
        string = "Last Trx Date",
        compute = '_compute_last_trx_date',
    )
    last_trx_date = fields.Date(
        string = "Last Trx Date",
        index = True,
        readonly = True,
        store = True,
    )
    is_late = fields.Char(
        string = "Is Late",
        index = True,
        readonly = True,
        store = True,
    )
    account_move_line_ids = fields.One2many(
        'account.move.line',
        'partner_id',
        String = 'Move Lines'
    )

    @api.onchange('account_move_line_ids')
    def _compute_last_trx_date(self):
        more60 = date.today() - timedelta(days = 60)
        more45 = date.today() - timedelta(days = 45)
        more30 = date.today() - timedelta(days = 30)

        for rec in self:
            test = self.env['account.move.line'].search([
                ('partner_id', '=', rec.id)
            ]).mapped('date')
            if test:
                rec.last_trx_date_auto = max(
                    self.env['account.move.line'].search([
                        ('partner_id', '=', rec.id)
                    ]).mapped('date')
                )
                rec.last_trx_date = rec.last_trx_date_auto

                if rec.last_trx_date:
                    if rec.credit == 0:
                        rec.is_late = 'zero balance'
                    else:
                        if rec.credit < 30:
                            rec.is_late = 'low balance'
                        elif rec.last_trx_date <= more60 and rec.credit >= 30:
                            rec.is_late = 'than 60 days'
                        elif rec.last_trx_date <= more45 and rec.credit >= 30:
                            rec.is_late = 'than 45 days'
                        elif rec.last_trx_date <= more30 and rec.credit >= 30:
                            rec.is_late = 'than 30 days'
                        else:
                            rec.is_late = 'safe period'
                else:
                    rec.is_late = 'no transaction'

            else:
                rec.last_trx_date = False
                rec.last_trx_date_auto = False
        return rec.last_trx_date, rec.last_trx_date_auto, rec.is_late
