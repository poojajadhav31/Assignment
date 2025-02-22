class MultiDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'users_app':
            return 'users_db'
        elif model._meta.app_label == 'orders_app':
            return 'orders_db'
        elif model._meta.app_label == 'products_app':
            return 'products_db'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'users_app':
            return db == 'users_db'
        elif app_label == 'orders_app':
            return db == 'orders_db'
        elif app_label == 'products_app':
            return db == 'products_db'
        return None
