class Pipup < Formula
  include Language::Python::Virtualenv

  desc "Update Python package versions in requirements.txt with exact versions from pip freeze"
  homepage "https://github.com/abozaralizadeh/pipup"
  url "https://github.com/abozaralizadeh/pipup/archive/v1.0.8.tar.gz"
  sha256 "1b6cca9556c66c95872fc65466de3e095c537b95c71aa06c36bd241fe601bd75"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/pipup", "--version"
  end
end
