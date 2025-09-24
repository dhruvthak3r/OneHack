

provider "aws" {
  profile = "onehack"  
  region  = "ap-south-1"
}

data "aws_vpc" "default" {
  default = true
}

data "aws_route_table" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
  filter {
    name   = "association.main"
    values = ["true"]
  }
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_internet_gateway" "default" {
  filter {
    name   = "attachment.vpc-id"
    values = [data.aws_vpc.default.id]
  }
}



resource "aws_instance" "onehack-infra" {
    ami = var.ec2_ami
    instance_type = var.ec2_instance_type
    vpc_security_group_ids = var.security_group_id_onehack
    key_name = var.ssh_key
    associate_public_ip_address = true

    tags = {
        Name = "onehack-backend-infra"
    }
    tags_all = {
      Name = "onehack-backend infra"
    }
}

resource "aws_db_instance" "onehack-db" {
  allocated_storage = 20
  db_name = ""
  engine = "mysql"
  identifier = "onehack-1"
  engine_version = "8.0.42"
  instance_class = "db.t4g.micro"
  username = "admin"
  password = var.onehack-db-password
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot = false
  storage_encrypted = true
}

resource "aws_security_group" "onehack" {
  name = "launch-wizard-1"
  description = "launch-wizard-1 created 2025-07-14T13:10:05.051Z"
  vpc_id = data.aws_vpc.default.id
  ingress {
    from_port = 22
    to_port =  22
    protocol =  "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

  }
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    
  }
  ingress {
    from_port = 8080
    to_port = 8080
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    
  }
  ingress {
    from_port = 5672
    to_port = 5672
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    
  }

  ingress {
    from_port = 15672
    to_port = 15672
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_security_group" "onehack-db-sg" {
  name = "default"
  description = "default VPC security group"
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port = 3306
    to_port = 3306
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
  from_port       = 0
  to_port         = 0
  protocol        = "-1"
  security_groups = var.security_group_id_rds
  }
}


output "ec2_instance_public_ip" {
  value = aws_instance.onehack-infra.public_ip
  
}
provider "vercel" {
  api_token = var.vercel_api_token
  team = var.vercel_team_id
  
}

resource "vercel_dns_record" "root" {
  domain = "onehack.live"
  name = ""
  type = "A"
  ttl = 60
  value = "216.198.79.1"
}

resource "vercel_dns_record" "backend" {
  domain = "onehack.live"
  name = "api"
  type = "A"
  ttl = 60
  value = aws_instance.onehack-infra.public_ip
  depends_on = [aws_instance.onehack-infra]
}

resource "vercel_dns_record" "worldwide" {
  domain = "onehack.live"
  name = "www"
  type = "CNAME"
  ttl = 60
  value = "db4f1dd88db68245.vercel-dns-017.com"
}