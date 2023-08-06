# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase


class ImageMapViewlet(ViewletBase):

    def update(self):
        self.imagemap = self.context.imagemap


    def render(self):
        return self.imagemap
