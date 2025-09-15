class Pipup < Formula
  include Language::Python::Virtualenv

  desc "Update Python package versions in requirements.txt with exact versions from pip freeze"
  homepage "https://github.com/abozaralizadeh/pipup"
  url "https://github.com/abozaralizadeh/pipup/archive/v1.1.1.tar.gz"
  sha256 "d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/pipup", "--version"
  end
end
