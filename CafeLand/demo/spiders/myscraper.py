import scrapy
import re

class MyscraperSpider(scrapy.Spider):
    name = "myscraper"
    allowed_domains = ["cafeland.vn"]
    start_urls = ["https://cafeland.vn/du-an/"]
    custom_settings = {
        # 'DOWNLOAD_DELAY': 2,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }

    page_count = 0

    def parse(self, response):
        self.page_count += 1
        self.logger.info(f"Đang duyệt trang {self.page_count}")

        projects = response.xpath("//li[contains(@class, 'hover-suggestions')]")

        for project in projects:
            try:
                project_type = project.xpath(".//span[@class='news-type-title']/text()").get()
                if project_type:
                    project_type = project_type.strip()

                project_name = project.xpath(".//a/@title").get()

                investor = project.xpath('.//span/a/text()').get()

                if investor:
                    investor = investor.strip().replace('Chủ đầu tư: ', '')

                # Lấy địa chỉ từ phần tử HTML
                map_location = project.xpath('.//div[@class="titleProjectSeo"]/text()[last()]').get()

                # Xử lý dữ liệu nếu có
                if map_location:
                    map_location = map_location.strip()
            
                    parts = map_location.split(',', 1)  
                    street = parts[0].strip() if len(parts) > 0 else None
                    city = parts[1].strip() if len(parts) > 1 else None
                else:
                    street = None
                    city = None
                status = response.xpath(".//span[@class='duan-dang-mo-ban']/text()").get()
                if status:
                    status = status.strip()


                detail_url = project.xpath('.//a/@href').get()
                if detail_url:
                    yield response.follow(detail_url, callback=self.parse_details, meta={
                        'project_type': project_type,
                        'project_name': project_name,
                        'street': street,
                        'city': city,
                        'investor': investor,
                        'status': status,

                    })

            except Exception as e:
                self.logger.error(f"Lỗi khi xử lý dự án: {e}")

        next_page = response.xpath("//a[contains(text(), '»')]/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

        self.logger.info(f"Hoàn tất duyệt trang {self.page_count}")

    def parse_details(self, response):
        date = response.xpath("//div[@class='info-date right']/span/text()").get()
        moTa = response.xpath("//div[@class='sevenPostDes']/text()").get()
 
        xpath_table = '//*[@id="sevenBoxNewContenDAtInfo"]//table'
        table_info = response.xpath(xpath_table)

        # Lấy diện tích 
        xpath_area = ".//tbody/tr[1]/td[2]/p"
        area = table_info.xpath(xpath_area)
        area = area.xpath('string()').get().replace('Tổng diện tích:', '') if area else ''
        
        # Lấy tổng đầu tư
        xpath_total_investment = ".//tbody/tr[2]/td[2]/p"
        total_investment = table_info.xpath(xpath_total_investment)
        total_investment = total_investment.xpath('string()').get().replace('Tổng vốn đầu tư:', '').strip() if total_investment else ''

        average_rating = response.xpath("//div[@class='overall-rating']//span[@id='avgrat']/text()").get()

        yield {
            'Loại dự án': response.meta.get('project_type'),
            'Tên dự án': response.meta.get('project_name'),
            'Đường': response.meta.get('street'),
            'Thành phố': response.meta.get('city'),
            'Chủ đầu tư': response.meta.get('investor'),
            'Trạng thái': response.meta.get('status'),
            'Diện tích:': area.strip() if area else 'unknown',
            'Ngày đăng': date.strip() if date else 'unknown',
            'Tổng vốn đầu tư': total_investment.strip() if total_investment else 'unknown',
            'Xếp hạng': average_rating.strip() if average_rating else 'unknown',
            'Mô tả': moTa.strip() if moTa else 'unknown',
        }


