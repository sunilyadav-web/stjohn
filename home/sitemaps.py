from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blog.models import Post

class StaticViewSitemap(Sitemap):
    def items(self):
        urls= ['index:index','index:about','index:certificate','index:vision-and-mission','index:result','index:apply','index:admitcard','index:idcard','index:contact','index:quiz','index:quiz-results','index:courses','index:health_science_courses','index:engineering_courses','index:management_courses','index:certified_courses','index:admission-regular','index:admission-online','index:admission-evening','exam:home','exam:exam-start','exam:exam-submission','users:register','users:login','users:logout','blog:home']
        return urls   
        
    def location(self, item):
        return reverse(item)

class BlogSiteMap(Sitemap):
    def items(self):
        return Post.objects.all()
    
    def location(self,item):
        return '/blog/%s' % (item.slug)
       