provider "aws" {
  profile = "personal"
  region = "eu-west-1"
}

variable "buckets" {
  type    = list(string)
}

variable "cnames" {
  type    = map(string)
}

data "aws_route53_zone" "mucana_org" {
  name = "mucana.org."
}

resource "aws_s3_bucket" "b" {
  for_each = toset(var.buckets)

  bucket = each.key
  region = "eu-west-1"
  acl = "public-read"

  website {
    index_document = "index.html"
  }

  tags = {
    Service = "mucana"
  }
}

resource "aws_route53_record" "r" {
  for_each = var.cnames

  zone_id = data.aws_route53_zone.mucana_org.id
  name    = each.key
  type    = "CNAME"

  alias {
    name    = aws_s3_bucket.b[each.value].website_domain
    zone_id = aws_s3_bucket.b[each.value].hosted_zone_id
    evaluate_target_health = false
  }
}
