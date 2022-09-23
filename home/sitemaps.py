from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
class StaticViewSitemap(Sitemap):
    def items(self):
        return ['index:index','index:about','index:certificate','index:vision-and-mission','index:result','index:apply','index:admitcard','index:idcard','index:contact','index:quiz','index:quiz-results','index:courses','index:health_science_courses','index:engineering_courses','index:management_courses','index:certified_courses','index:admission-regular','index:admission-online','index:admission-evening','exam:home','exam:exam-start','exam:exam-submission','users:register','users:login','users:logout']
    def location(self, item):
        return reverse(item)