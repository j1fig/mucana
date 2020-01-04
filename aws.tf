provider "aws" {
  profile = "personal"
  region = "eu-west-1"
}

variable "buckets" {
  type    = list(string)
}

resource "aws_s3_bucket" "b" {
  for_each = toset(var.buckets)
  bucket = each.key
}
