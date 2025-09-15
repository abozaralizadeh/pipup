class Pipup < Formula
  include Language::Python::Virtualenv

  desc "Update Python package versions in requirements.txt with exact versions from pip freeze"
  homepage "https://github.com/abozaralizadeh/pipup"
  url "https://github.com/abozaralizadeh/pipup/archive/v1.0.2.tar.gz"
  sha256 "f4818553f9b10eddb143747591a0890cc405a93debdb24c03cd386b4681e4206"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/pipup", "--version"
  end
end
