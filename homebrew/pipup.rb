class Pipup < Formula
  include Language::Python::Virtualenv

  desc "Update Python package versions in requirements.txt with exact versions from pip freeze"
  homepage "https://github.com/abozaralizadeh/pipup"
  url "https://github.com/abozaralizadeh/pipup/archive/v1.0.1.tar.gz"
  sha256 ""  # This will be filled in when the tarball is created
  version "1.0.1"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/pipup", "--version"
  end
end
