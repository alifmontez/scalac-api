#Create and bootstrap instance
resource "aws_instance" "appserver" {
  ami                         = data.aws_ssm_parameter.my-ami.value
  instance_type               = "t3.micro"
  key_name                    = aws_key_pair.my-key.key_name
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.sg.id]
  subnet_id                   = aws_subnet.subnet.id
  provisioner "remote-exec" {
    inline = [
      "sudo yum -y update",
      "sudo amazon-linux-extras enable ansible2",
      "sudo yum install -y ansible",
      "sudo yum install -y docker",
      "sudo yum install -y git",
      "sudo yum install -y java-1.8.0-openjdk",
      "sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo",
      "sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key",
      "sudo yum install -y jenkins",
      "sudo service jenkins start"
    ]
    connection {
      type        = "ssh"
      user        = "ec2-user"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }
  tags = {
    Name = "appserver"
  }
}