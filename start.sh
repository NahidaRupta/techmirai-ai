#!/bin/bash

# TechMirai AI - Quick Start Script
# This script will set up and run the complete application

set -e

echo "========================================="
echo "  TechMirai AI - Quick Start Setup"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker is installed"
echo "✓ Docker Compose is installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating environment configuration..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env with your email settings for contact form notifications"
    echo ""
fi

# Ask if user wants to start now
read -p "Do you want to start the application now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Starting TechMirai AI application..."
    echo ""
    
    # Start with Docker Compose
    docker-compose up -d
    
    echo ""
    echo "========================================="
    echo "  ✅ TechMirai AI is now running!"
    echo "========================================="
    echo ""
    echo "Access your application:"
    echo "  🌐 Website:  http://localhost"
    echo "  🔧 API:      http://localhost:8000"
    echo "  📚 API Docs: http://localhost:8000/docs"
    echo ""
    echo "To view logs:"
    echo "  docker-compose logs -f"
    echo ""
    echo "To stop:"
    echo "  docker-compose down"
    echo ""
    echo "⚠️  Remember to configure email settings in backend/.env"
    echo "    for contact form notifications to work!"
    echo ""
else
    echo ""
    echo "Setup files are ready. To start manually, run:"
    echo "  docker-compose up -d"
    echo ""
fi