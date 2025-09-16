class Pipup < Formula
  include Language::Python::Virtualenv

  desc "Update Python package versions in requirements.txt with exact versions from pip freeze"
  homepage "https://github.com/abozaralizadeh/pipup"
  url "https://github.com/abozaralizadeh/pipup/archive/v1.1.1.tar.gz"
  sha256 "073aeaf4caffb7643f394c0038ccf8f5a729a65e701e4dad7dd462a2dfc6175c"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/pipup", "--version"
  end
end
