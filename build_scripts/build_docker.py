import tomli
import subprocess
import sys
import argparse


def setup_buildx():
    """Setup docker buildx builder for multi-arch builds"""
    # Create a new builder instance if it doesn't exist
    create_builder_cmd = [
        "docker", "buildx", "create", "--name", "multiarch", "--use"
    ]
    try:
        subprocess.run(create_builder_cmd, check=True)
    except subprocess.CalledProcessError:
        # Builder might already exist, try to use it
        subprocess.run(["docker", "buildx", "use", "multiarch"], check=True)

    # Bootstrap the builder
    subprocess.run(["docker", "buildx", "inspect", "--bootstrap"], check=True)


def main():
    parser = argparse.ArgumentParser(description='Build Docker images for multiple architectures')
    parser.add_argument('--platforms', default='linux/amd64,linux/arm64,linux/arm/v7',
                       help='Comma-separated list of platforms to build for')
    parser.add_argument('--push', action='store_true',
                       help='Push images to registry after building')
    args = parser.parse_args()

    # Read pyproject.toml
    with open("pyproject.toml", "rb") as f:
        pyproject = tomli.load(f)

    # Extract version, Python version, and author
    version = pyproject["tool"]["poetry"]["version"]
    python_version = pyproject["tool"]["poetry"]["dependencies"]["python"].strip(
        "^")
    # Extract username from authors field (format: ["Name <email>"])
    author = pyproject["tool"]["poetry"]["authors"][0]
    username = author.split("<")[0].strip().lower()

    # Prepare Docker image name and tags
    image_name = f"{username}/qbittorrent-add-trackers"
    tags = [
        f"{image_name}:latest",
        f"{image_name}:{version}"
    ]

    # Setup buildx for multi-arch builds
    setup_buildx()

    # Prepare tag arguments
    tag_args = []
    for tag in tags:
        tag_args.extend(["-t", tag])

    # Build Docker image for multiple platforms
    build_cmd = [
        "docker", "buildx", "build",
        "--platform", args.platforms,
        "--build-arg", f"PYTHON_VERSION={python_version}",
    ]
    
    # Add tags
    build_cmd.extend(tag_args)
    
    # When building multi-arch without push, we need to use --output=type=image,push=false
    # When pushing, use --push
    if args.push:
        build_cmd.append("--push")
    else:
        build_cmd.append("--output=type=image,push=false")
    
    # Add build context
    build_cmd.append(".")

    print(f"Building Docker image: {' '.join(build_cmd)}")
    try:
        result = subprocess.run(build_cmd, check=True)
        platforms_list = args.platforms.split(',')
        print(f"Docker image built successfully for platforms: {', '.join(platforms_list)}")
        print(f"Tags: {', '.join(tags)}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to build Docker image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
